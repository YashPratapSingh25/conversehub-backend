from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator, cast
from fastapi import FastAPI
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from src.auth.models.refresh_token_model import RefreshToken
from src.auth.models.user_model import UserAuth
from src.core.db import session_maker
from src.core.logger import logger

scheduler = None

async def clear_refresh_tokens():
    logger.info("Clearing Refresh Tokens")
    async with session_maker() as session:
        await session.execute(
            delete(RefreshToken)
            .where((RefreshToken.exp < datetime.now(timezone.utc)) | (RefreshToken.used.is_(True)))
        )

        await session.commit()
    
async def init_scheduler():
    global scheduler
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        func=clear_refresh_tokens,
        trigger=IntervalTrigger(days=1),
        id="clear_refresh_tokens",
        name="Clear used and expired tokens",
        replace_existing=True,
        max_instances=1
    )

async def close_scheduler():
    global scheduler
    scheduler.shutdown()
    scheduler = None