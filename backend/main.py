from fastapi import FastAPI, UploadFile, File
import tempfile
import os

from src.resume_parser import extract_text_from_pdf, extract_email, extract_phone
from src.skill_extractor import extract_skills
from src.job_recommender import recommend_jobs
from backend.schemas import ResumeResponse

app = FastAPI(
    title="Resume Parser & Job Recommender API",
    description= "AI-powered  resume parsing and job recommendatio service",
    version='1.0.0'
)
SKILLS_DB = [
    "Python", "Machine Learning", "Deep Learning", "SQL", "Pandas",
    "Excel", "TensorFlow", "PyTorch", "NLP", "Data Analysis"
]

JOB_DATA = {
    "Data Scientist": "Python Machine Learning SQL Pandas Statistics",
    "Machine Learning Engineer": "Python Machine Learning Deep Learning TensorFlow PyTorch",
    "Data Analyst": "Python SQL Excel Data Analysis Visualization",
    "AI Engineer": "Python Deep Learning TensorFlow PyTorch NLP",
    "Backend Developer": "Python Django REST API SQL"
}

@app.post("/analyze-resume", response_model=ResumeResponse)
async def analyze_resume(file: UploadFile = File(...)):
    # save uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        temp_path = tmp.name
    # extract data
    resume_text = extract_text_from_pdf(temp_path)
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    skills = extract_skills(resume_text, SKILLS_DB)
    job_results = recommend_jobs(skills, JOB_DATA)
    
    os.remove(temp_path)
    
    return ResumeResponse(
        email= email,
        phone= phone,
        skills= skills,
        recommended_jobs= [job for job, _ in job_results]
    )