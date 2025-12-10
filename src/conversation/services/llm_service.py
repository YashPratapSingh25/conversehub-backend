import asyncio
import base64
import json
import os
import re
import google.genai as genai
from google.genai import types
from src.conversation.schemas.gemini_response_schema import GeminiResponse
from src.core.config import settings
from pathlib import Path
from src.core.logger import logger

def get_system_instruction(
    resume_text : str | None = None,
    job_description : str | None = None,
    topic_tags : list | None = None,
    last_api_reply : str | None = None
) -> str:
    prompt_file_path = Path(__file__).parent.parent.parent / "core" / "prompts" / "interviewer_sys_instruction.txt"
    basic_instruction = prompt_file_path.read_text(encoding="utf-8")

    resume_text = f"\n\n<Resume Text :->\n{resume_text}\n" if resume_text else ""
    job_description = f"\n\n<Job Description :->\n{job_description}\n" if job_description else ""
    last_api_reply = f"\n\n<Last AI Reply :->\n{last_api_reply}\n" if last_api_reply else ""

    system_instruction = basic_instruction + resume_text + job_description + last_api_reply + "\n<Topic tags :->\n" + str(topic_tags)
    return system_instruction

async def generate_llm_response(transcription : str, resume_text : str | None = None, job_description : str = None, topic_tags : list | None = None, last_api_reply : str | None = None) -> dict:
    client = genai.Client(
        api_key=settings.GEMINI_API_KEY,
    )

    model = settings.GEMINI_MODEL

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=transcription),
            ],
        )
    ]
    
    tools = [
        types.Tool(googleSearch=types.GoogleSearch()),
    ]
    
    system_instruction = get_system_instruction(resume_text, job_description, topic_tags, last_api_reply)
    
    generate_content_config = types.GenerateContentConfig(
        tools=tools,
        system_instruction=[
            types.Part.from_text(text=system_instruction),
        ],
        response_mime_type = "application/json",
        response_schema = GeminiResponse,
    )

    response = await asyncio.to_thread(
        lambda : client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
    )

    return json.loads(response.text.strip())