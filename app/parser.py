import os
import uuid
from fastapi import UploadFile
import aiofiles
from docx import Document
import fitz

async def extract_text_from_file(file: UploadFile) -> str:
    filename = file.filename
    extension = os.path.splitext(filename)[1].lower()
    temp_path = f"temp_{uuid.uuid4().hex}{extension}"

    async with aiofiles.open(temp_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    if file.filename.endswith('.docx'):
        text = extract_docx(temp_path)
        os.remove(temp_path)
    elif file.filename.endswith('.txt'):
        text = extract_txt(temp_path)
        os.remove(temp_path)
    elif filename.endswith(".pdf"):
        text = extract_pdf(temp_path)
        os.remove(temp_path)
    else:
        os.remove(temp_path)
        raise ValueError("Unsupported file type. Please upload a .docx, .txt, or .pdf file.")

    return text

def extract_docx(file_path: str) -> str:
    doc = Document(file_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return '\n'.join(text)

def extract_txt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_pdf(file_path: str) -> str: 
    doc = fitz.open(file_path)
    text = []
    for page in doc:
        text.append(page.get_text())
    return '\n'.join(text)
