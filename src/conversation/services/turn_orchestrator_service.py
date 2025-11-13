import asyncio
from datetime import datetime, timezone
import os
from uuid import UUID
import uuid
from fastapi import UploadFile, BackgroundTasks
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified
from src.conversation.models.session_model import Session
from src.conversation.models.turn_model import Turn
from src.conversation.services.blob_service import upload_file_and_get_sas
from src.conversation.services.speech_generation_service import generate_tts_audio
from src.conversation.services.temp_file_service import create_temp_file_from_req
from src.conversation.services.vocal_assessment_service import analyze_speech
from src.conversation.services.llm_service import generate_llm_response
from src.conversation.services.transcription_service import transcribe_audio
from src.core.exceptions_utils.exceptions import BadRequestError
from src.core.logger import logger

async def turn_orchestrator(
    audio_file: UploadFile | None,
    session_id: UUID,
    db_session: AsyncSession,
    background_tasks : BackgroundTasks
):
    if not audio_file:
        raise BadRequestError("No audio file found")

    content = await audio_file.read(1)
    if not content:
        raise BadRequestError("Audio file is empty")
    await audio_file.seek(0)

    turn_id = uuid.uuid4()

    session_db_result = await db_session.execute(
        select(Session).where(Session.id == session_id)
    )

    session = session_db_result.scalar_one_or_none()

    if session is None:
        raise BadRequestError("Invalid session ID")
    
    details = session.details

    resume_text = details.get("resume_text")
    job_description = details.get("job_description")
    topic_tags = details.get("topic_tags")

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

    audio_file_path = await create_temp_file_from_req(audio_file, True)

    transcription_task = asyncio.create_task(transcribe_audio(audio_file_path))
    user_speech_sas_task = asyncio.create_task(upload_file_and_get_sas(
        user_id=session.user_id,
        session_id=session.id,
        turn_id=turn_id,
        file_path=audio_file_path,
        user=True
    ))

    transcription, user_speech_sas = await asyncio.gather(transcription_task, user_speech_sas_task)

    llm_response_task = asyncio.create_task(generate_llm_response(transcription, resume_text, job_description, topic_tags, last_ai_reply))

    llm_response = await llm_response_task

    topic = llm_response.get("topic")
    if topic and topic not in topic_tags:
        session.details["topic_tags"].append(topic)
        flag_modified(session, "details")

    ai_reply = llm_response.get("reply", "")

    ai_speech_file_path = await generate_tts_audio(ai_reply)
    ai_speech_sas_task = asyncio.create_task(upload_file_and_get_sas(
        user_id=session.user_id,
        session_id=session.id,
        turn_id=turn_id,
        file_path=ai_speech_file_path,
        user=False
    ))

    ai_speech_sas = await ai_speech_sas_task

    os.unlink(ai_speech_file_path)
    os.unlink(audio_file_path)

    db_session.add(session)
    await db_session.commit()

    scores = {**(llm_response["feedback"]["scores"])}
        
    feedback = {
        **llm_response.get("feedback"),
        "scores": scores
    }

    new_turn = Turn(
        id=turn_id,
        session_id=session_id,
        user_text=transcription,
        ai_text=ai_reply,
        feedback=feedback,
        status="completed"   
    )

    db_session.add(new_turn)
    await db_session.commit()

    result = {
        "turn_id": str(turn_id),
        "transcription": transcription,
        "llm_response": llm_response,
        "user_speech": user_speech_sas,
        "ai_speech": ai_speech_sas
    }

    return result