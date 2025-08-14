import httpx
import aiofiles
from src.core.config import settings

async def transcribe_audio(
    audio_file_path : str
) -> str:
    
    API_KEY = settings.DEEPGRAM_API_KEY
    url = "https://api.deepgram.com/v1/listen"
    headers = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "audio/*"
    }
    params = {
        "model": "nova-2",
        "punctuate": True,
        "smart_format": True,
        "filler_words": True
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        async with aiofiles.open(audio_file_path, mode="rb") as audio_file:
            audio_content = await audio_file.read()

            response = await client.post(
                url=url,
                headers=headers,
                content=audio_content,
                params=params
            )

    json_response = response.json()
    transcript = json_response["results"]["channels"][0]["alternatives"][0]["transcript"]
    return transcript