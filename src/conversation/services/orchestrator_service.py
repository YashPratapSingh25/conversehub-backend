import os
import time
from fastapi import UploadFile
from src.conversation.services.audio_file_service import create_audio_file
from src.conversation.services.transcription_service import transcribe_audio

async def orchestrator(
    audio_file : UploadFile
):
    start_time = time.time()
    audio_file_path = await create_audio_file(audio_file)
    transcription = await transcribe_audio(audio_file_path)
    os.unlink(audio_file_path)
    end_time = time.time()
    time_taken = end_time - start_time
    result = {
        "transcription": transcription
    }
    return result