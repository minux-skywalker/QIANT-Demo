from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from app.scorer import score_resume
from app.parser import extract_text_from_file
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = FastAPI()

# CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/upload")
async def upload_file(jd: UploadFile = File(...), resumes:List[UploadFile] = File(...)):
    jd_text = await extract_text_from_file(jd)

    results = []

    for resume in resumes:
        resume_text = await extract_text_from_file(resume)
        score,reason=score_resume(jd_text, resume_text)
        results.append({
            "resume_name": resume.filename,
            "score": score,
            "reason": reason
        })

    return {"results": results}