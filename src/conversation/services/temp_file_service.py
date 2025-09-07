import os
from pathlib import Path
import aiofiles
from fastapi import UploadFile
import tempfile
from pydub import AudioSegment
from src.core.logger import logger

tmp_directory = tempfile.gettempdir()

async def create_temp_file(file : UploadFile, is_audio_file : bool = False):
    suffix = Path(file.filename).suffix
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=tmp_directory)
    temp_path = temp_file.name
    temp_file.close()

    async with aiofiles.open(temp_path, "wb") as new_file:
        content = await file.read()
        await new_file.write(content)

    if suffix.lower() != ".wav" and is_audio_file:
        wav_path = temp_file.name + ".wav"
        audio = AudioSegment.from_file(temp_path)
        
        audio.export(wav_path, format="wav")
        
        os.remove(temp_path)
        
        return wav_path

    return temp_path