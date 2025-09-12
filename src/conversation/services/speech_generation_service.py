import httpx
import asyncio
from src.conversation.services.temp_file_service import create_temp_file_from_audio
from src.core.config import settings
from src.core.logger import logger

async def generate_speech(text : str) -> str:
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            url=settings.ELEVENLABS_URL,
            headers={
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": settings.ELEVENLABS_API_KEY
            },
            json={
                "text": text,
                "model_id": "eleven_flash_v2_5"
            }
        )
    
    file_path = await create_temp_file_from_audio(response.content)
    return file_path