import asyncio
import os
from fastapi import UploadFile
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.user_model import UserAuth
from src.conversation.models.session_model import Session
from src.conversation.models.turn_model import Turn
from src.conversation.schemas.session_response_schema import CreateSessionResponseSchema
from src.conversation.services.resume_extractor import extract_resume_text
from src.conversation.services.temp_file_service import create_temp_file
from src.core.exceptions_utils.exceptions import BadRequestError

async def start_session(
    session_name : str,
    user : UserAuth,
    resume : UploadFile | None,
    db_session : AsyncSession,
    job_description : str | None = None,
    mode : str = "interview",
):
    result = await db_session.execute(
        select(exists().where(Session.session_name == session_name))
    )

    session_exists = result.scalar()

    if session_exists:
        raise BadRequestError("Session with this name already exists")

    if resume:
        resume_path = await create_temp_file(resume)
        resume_text = await asyncio.to_thread(extract_resume_text, resume_path)

    details = {
        "resume_text": resume_text,
        "job_description": job_description,
        "topic_tags" : []
    }

    new_session = Session(
        user_id = user.id,
        session_name = session_name,
        mode = mode,
        details = details,
    )

    db_session.add(new_session)
    await db_session.commit()
    await db_session.refresh(new_session)

    start_turn = Turn(
        session_id = new_session.id,
        user_text = "",
        ai_text = "Good morning. Let's start with the interview. We can start with your introduction whenever you are ready.",
        feedback = {},
        user_speech_link = "",
        ai_speech_link = ""   
    )
    db_session.add(start_turn)
    await db_session.commit()
    await db_session.refresh(start_turn)

    os.unlink(resume_path)

    return CreateSessionResponseSchema.model_validate(new_session)