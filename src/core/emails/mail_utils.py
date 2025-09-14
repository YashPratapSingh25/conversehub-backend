from pathlib import Path
from fastapi import BackgroundTasks
from jinja2 import Template
from pydantic import EmailStr
from src.core.emails.mail_config import send_email

curr_dir = Path(__file__).resolve().parent
template_path = curr_dir / "templates" / "otp_email.html"
template_content = Path(template_path).read_text()

def send_otp_mail(
    email : EmailStr,
    subject : str,
    otp : str,
    background_tasks : BackgroundTasks
):
    html = Template(template_content).render(
        username=email,
        otp=otp
    )
    
    background_tasks.add_task(send_email, email, subject, html)