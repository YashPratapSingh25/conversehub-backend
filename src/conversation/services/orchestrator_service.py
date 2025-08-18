import os
import time
from fastapi import UploadFile
from src.conversation.services.audio_file_service import create_audio_file
from src.conversation.services.assessment_service import analyze_speech
from src.conversation.services.llm_service import generate_llm_response
from src.conversation.services.transcription_service import transcribe_audio

async def orchestrator(
    audio_file : UploadFile
):
    
    audio_file_path = await create_audio_file(audio_file)
    transcription = await transcribe_audio(audio_file_path)
    vocal_assessment = analyze_speech(audio_file_path, transcription)
    llm_response = generate_llm_response(transcription)
    result = {
        "transcription": transcription,
        "vocal_assessment": vocal_assessment,
        "llm_response": llm_response
    }
    os.unlink(audio_file_path)
    return result