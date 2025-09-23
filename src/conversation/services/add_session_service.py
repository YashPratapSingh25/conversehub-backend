import asyncio
from datetime import datetime, timezone
import os
import uuid
from fastapi import UploadFile
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models.user_model import UserAuth
from src.conversation.models.session_model import Session
from src.conversation.models.turn_model import Turn
from src.conversation.services.blob_service import upload_file_and_get_sas
from src.conversation.services.resume_extractor import extract_resume_text
from src.conversation.services.temp_file_service import create_temp_file_from_req
from src.core.exceptions_utils.exceptions import BadRequestError
from src.core.config import settings

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

    resume_path = ""
    resume_text = ""
    if resume:
        resume_path = await create_temp_file_from_req(resume)
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

    turn_id = uuid.uuid4()

    ai_text = "Greetings. Let's start with the interview. We can start with your introduction whenever you are ready."
    
    start_turn = Turn(
        id = turn_id,
        session_id = new_session.id,
        user_text = "",
        ai_text = ai_text,
        feedback = {}
    )

    db_session.add(start_turn)
    await db_session.commit()
    await db_session.refresh(start_turn)

    if resume_path != "":
        os.unlink(resume_path)

    return {
        "id" : new_session.id,
        "session_name": session_name,
        "mode": mode,
        "created_at": datetime.now(timezone.utc),
        "ai_text": ai_text,
        "ai_intro": settings.INTERVIEW_AI_INTRO,
        "status": "completed"
    }