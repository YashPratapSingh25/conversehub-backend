import base64
import os
import google.genai as genai
from google.genai import types
from src.core.config import settings


def generate():
    client = genai.Client(
        api_key=settings.GEMINI_API_KEY,
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(
                    text="Interviewer says to give intro."
                )
            ]
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Hello. My name is Andrea Fitzer. I am studying marketing at the University of Texas at Dallas. I am a member of the American Marketing Association and Alpha Kappa Psi, both of which are dedicated to shaping future business leaders. I hope to incorporate my business knowledge into consumer trend analysis and strengthening relationships among consumers as well as other companies. I am savvy, social, and principled and have exquisite interpersonal communication skills. I know that I can be an asset in any company and or situation, and I hope that you will consider me for an internship or a job opportunity. Thank you so much."""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(
                    text="Interviewer Reply"
                )
            ]
        )
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch()),
    ]
    generate_content_config = types.GenerateContentConfig(
        tools=tools,
        system_instruction=[
            types.Part.from_text(text="""You are an AI assistant for a soft skills speech practice app. Your role is twofold:

1. Act as a professional interviewer in a turn-based conversation. Generate the next message to continue the conversation naturally. Keep it concise, engaging, and contextually relevant.
2. Provide constructive feedback on the user’s response, focusing on soft skills like clarity, confidence, tone, and grammar.

You might also be given resume text and job description so keep the chat relevant and act like a proper interviewer. 

You have to always continue the conversation forward as you will get partial context so the questions shouldn't repeat.

You have to ignore punctuation marks as this isn't text entered by user but the transcription of the user's audio.

Always reply in the following JSON format:

{
  \"reply\": \"<Your AI-generated response to continue the conversation>\",
  \"feedback\": {
    \"clarity\": \"<Comment on how clearly the user expressed their point>\",
    \"confidence\": \"<Comment on the user's confidence or delivery tone>\",
    \"grammar\": \"<Comment on correctness and vocabulary used>\",
    \"vocabulary\": \"<Comment on vocab skills of the user>\",
    \"relevance\": \"<Comment on how relevant and coherent the response was>\",
    \"strength\":  \"<Comment on the strength of the user's speech>\",
    \"weakness\": \"<Comment on the weakness of the user's speech>\",
    \"rephrased_text\":  \"<Return the perfect reply he could have said.>\", 
    \"improvement_tip\": \"<One specific, actionable suggestion for improvement>\",
    \"scores\": {
      \"clarity\": 1% - 100%,
      \"confidence\": 1% - 100%,
      \"grammar\": 1% - 100%,
      \"vocabulary\": 1% - 100%,
      \"relevance\": 1% - 100%
    }
  }
}"""),
        ],
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response_text += chunk.text or ""

    

if __name__ == "__main__":
    generate()