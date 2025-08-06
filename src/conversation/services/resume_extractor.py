import os
import pdfplumber
import docx
from pathlib import Path
from typing import Union

def extract_text_from_pdf(file_path: Union[str, Path]) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.strip()

def extract_text_from_docx(file_path: Union[str, Path]) -> str:
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

def extract_text_from_txt(file_path: Union[str, Path]) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

def extract_resume_text(file_path: Union[str, Path]) -> str:
    file_path = Path(file_path)
    ext = file_path.suffix.lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

resume_text = extract_resume_text(r"c:\Users\ASUS\Downloads\Yash Pratap Singh POD Resume(Incorrect Education).pdf")
print(resume_text)