from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator, cast
from fastapi import FastAPI
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from src.auth.models.otp_model import Otp
from src.auth.models.refresh_token_model import RefreshToken
from src.auth.models.user_model import UserAuth
from src.core.db import session_maker

scheduler = None

async def clear_otps():
    async with session_maker() as session:
        await session.execute(
            delete(Otp)
            .where(
                (Otp.used == True) | (Otp.exp < datetime.now(timezone.utc))
            )
        )

        await session.commit()   

async def clear_unregistered_users():
    delete_time = datetime.now(timezone.utc) - timedelta(days=1)

    async with session_maker() as session:
        await session.execute(
            delete(UserAuth)
            .where(UserAuth.verified == False)
            .where(UserAuth.created_at < delete_time)
        )
        
        await session.commit()

async def clear_refresh_tokens():
    async with session_maker() as session:
        await session.execute(
            delete(RefreshToken)
            .where(RefreshToken.exp < datetime.now(timezone.utc) | (RefreshToken.used == True))
        )

        await session.commit()
    
async def init_scheduler():
    global scheduler
    scheduler = AsyncIOScheduler()

    

    scheduler.add_job(
        clear_otps,
        trigger=IntervalTrigger(minutes=10),
        id="clear_otps_job",
        name="Clear used and expired OTPs",
        replace_existing=True,
        max_instances=1 
    )

    scheduler.add_job(
        func=clear_unregistered_users,
        trigger=IntervalTrigger(days=1),
        id="clear_unregistered_users",
        name="Clear Unregisterd Users",
        replace_existing=True,
        max_instances=1
    )

    scheduler.add_job(
        func=clear_refresh_tokens,
        trigger=IntervalTrigger(days=1),
        id="clear_refresh_tokens",
        name="Clear used and expired tokens",
        replace_existing=True,
        max_instances=1
    )

    scheduler.start()

async def close_scheduler():
    global scheduler
    scheduler.shutdown()
    scheduler = None