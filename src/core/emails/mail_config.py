import os
from pydantic import EmailStr
import resend
from src.core.config import settings

resend.api_key = settings.RESEND_API_KEY

def send_email(to_email: EmailStr, subject: str, html_content: str):
    try:
        params = {
            "from": settings.MAIL_FROM,
            "to": [to_email],
            "subject": subject,
            "html": html_content,
        }
        
        email = resend.Emails.send(params)
        return {"status": "success", "id": email.get("id")}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}