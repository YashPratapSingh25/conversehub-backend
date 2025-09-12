import os
from pathlib import Path
import aiofiles
from fastapi import UploadFile
import tempfile
from httpx import Response
from pydub import AudioSegment
from src.core.logger import logger
import asyncio

tmp_directory = tempfile.gettempdir()

async def convert_to_wav(temp_path: str) -> str:
    wav_path = temp_path + ".wav"
    
    def convert():
        audio = AudioSegment.from_file(temp_path)
        audio.export(wav_path, format="wav")
        os.remove(temp_path)

    await asyncio.to_thread(convert)
    
    return wav_path

async def create_temp_file_from_req(file : UploadFile, is_audio_file : bool = False):
    suffix = Path(file.filename).suffix
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=tmp_directory)
    temp_path = temp_file.name
    temp_file.close()

    async with aiofiles.open(temp_path, "wb") as new_file:
        content = await file.read()
        await new_file.write(content)

    if (suffix.lower() != ".wav" or suffix.lower() != ".mp3") and is_audio_file:
        return await convert_to_wav(temp_path)

    return temp_path

async def create_temp_file_from_audio(response_content, suffix : str = ".wav"):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=tmp_directory)
    temp_path = temp_file.name
    temp_file.close()

    async with aiofiles.open(temp_path, "wb") as new_file:
        await new_file.write(response_content)

    return temp_path