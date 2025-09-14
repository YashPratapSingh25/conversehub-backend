import base64
import mimetypes
import os
import re
import struct
from google import genai
from google.genai import types
import asyncio
from src.conversation.services.temp_file_service import create_temp_file_from_audio
from src.core.config import settings

async def generate_tts_audio(text_prompt: str, voice_name: str = "Autonoe") -> str:
    client = genai.Client(
        api_key=settings.GEMINI_API_KEY,
    )

    model = "gemini-2.5-flash-preview-tts"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=text_prompt),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name=voice_name
                )
            )
        ),
    )

    combined_audio_data = b""
    detected_mime_type = None
    
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue
            
        part = chunk.candidates[0].content.parts[0]
        
        if part.inline_data and part.inline_data.data:
            inline_data = part.inline_data
            combined_audio_data += inline_data.data
            
            if detected_mime_type is None:
                detected_mime_type = inline_data.mime_type
        elif hasattr(part, 'text') and part.text:
            print(f"Received text: {part.text}")
    
    if not combined_audio_data:
        raise ValueError("No audio data received from the API")
    
    file_extension = mimetypes.guess_extension(detected_mime_type)
    final_audio_data = combined_audio_data
    
    if file_extension is None or file_extension not in ['.wav', '.mp3']:
        file_extension = ".wav"
        final_audio_data = convert_to_wav(combined_audio_data, detected_mime_type)
    
    temp_file_path = await create_temp_file_from_audio(
        final_audio_data, 
        suffix=file_extension
    )
    
    return temp_file_path


def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",          # ChunkID
        chunk_size,       # ChunkSize (total file size - 8 bytes)
        b"WAVE",          # Format
        b"fmt ",          # Subchunk1ID
        16,               # Subchunk1Size (16 for PCM)
        1,                # AudioFormat (1 for PCM)
        num_channels,     # NumChannels
        sample_rate,      # SampleRate
        byte_rate,        # ByteRate
        block_align,      # BlockAlign
        bits_per_sample,  # BitsPerSample
        b"data",          # Subchunk2ID
        data_size         # Subchunk2Size (size of audio data)
    )
    return header + audio_data


def parse_audio_mime_type(mime_type: str) -> dict[str, int]:
    bits_per_sample = 16
    rate = 24000

    if not mime_type:
        return {"bits_per_sample": bits_per_sample, "rate": rate}

    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate_str = param.split("=", 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                pass
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass

    return {"bits_per_sample": bits_per_sample, "rate": rate}