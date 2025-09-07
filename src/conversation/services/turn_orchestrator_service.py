import asyncio
import os
from pathlib import Path
import time
from uuid import UUID
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified
from src.conversation.models.session_model import Session
from src.conversation.models.turn_model import Turn
from src.conversation.services.temp_file_service import create_temp_file
from src.conversation.services.vocal_assessment_service import analyze_speech
from src.conversation.services.llm_service import generate_llm_response
from src.conversation.services.transcription_service import transcribe_audio
from src.core.exceptions_utils.exceptions import BadRequestError
from src.core.logger import logger

async def turn_orchestrator(
    audio_file : UploadFile | None,
    session_id : UUID,
    db_session : AsyncSession
):
    
    # return only transcription and user_audio_link in response. save the rest of the content in the db and do polling from frontend

    if not audio_file:
        raise BadRequestError("No audio file found")

    content = await audio_file.read(1)
    if not content:
        raise BadRequestError("Audio file is empty")
    await audio_file.seek(0)

    audio_file_path = await create_temp_file(audio_file, True)
    logger.debug("Audio file generated")
    transcription = await transcribe_audio(audio_file_path)
    logger.debug(f"Transcription Done\n{transcription}")

    session_db_result = await db_session.execute(
        select(Session)
        .where(Session.id == session_id)
    )

    session = session_db_result.scalar_one_or_none()

    if session is None:
        raise BadRequestError("Invalid session ID")
    
    details = session.details

    resume_text = details.get("resume_text")
    job_description = details.get("job_description")
    topic_tags : list = details.get("topic_tags")


    turn_db_result = await db_session.execute(
        select(Turn)
        .where(Turn.session_id == session_id)
        .order_by(Turn.created_at.desc())
        .limit(1)
    )

    last_turn = turn_db_result.scalar_one_or_none()

    last_ai_reply = ""
    if last_turn:
        last_ai_reply = last_turn.ai_text

    vocal_assessment_task = analyze_speech(audio_file_path, transcription)
    llm_response_task = generate_llm_response(transcription, resume_text, job_description, topic_tags, last_ai_reply)
    
    logger.debug("Going to Azure and Gemini")
    vocal_assessment, llm_response = await asyncio.gather(vocal_assessment_task, llm_response_task)
    logger.debug("Result came from Azure and Gemini")
    
    topic = llm_response.get("topic")
    if topic and topic not in topic_tags:
        session.details["topic_tags"].append(topic)
        flag_modified(session, "details")

    ai_reply = llm_response.get("reply", "")

    scores = {**(llm_response["feedback"]["scores"])}

    feedback = {
        **llm_response.get("feedback")
    }
    
    if vocal_assessment:
        scores.update({
            "duration": vocal_assessment.get("duration"),
            "words_per_min": vocal_assessment.get("words_per_min"),
            "pronunciation_score": vocal_assessment.get("pronunciation_score"),
            "accuracy_score": vocal_assessment.get("accuracy_score"),
            "fluency_score": vocal_assessment.get("fluency_score")
        })
    
    turn = Turn(
        session_id = session_id,
        user_text = transcription,
        ai_text = ai_reply,
        feedback = feedback,
        user_speech_link = "",
        ai_speech_link = ""
    )

    db_session.add(session)
    db_session.add(turn)
    await db_session.commit()
    await db_session.refresh(session)
    await db_session.refresh(turn)

    result = {
        "transcription": transcription,
        "vocal_assessment": vocal_assessment,
        "llm_response": llm_response
    }

    os.unlink(audio_file_path)
    logger.debug(str(result))
    return result