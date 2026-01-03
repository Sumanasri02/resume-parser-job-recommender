from src.resume_parser import extract_text_from_pdf, extract_email, extract_phone
from src.skill_extractor import extract_skills
from src.job_recommender import recommend_jobs

RESUME_PATH = "resumes/Sumanasri_k_Resume.pdf"

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

def main():
    print("\n Parsing Resume")
    resume_text = extract_text_from_pdf(RESUME_PATH)
    
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    
    print(f"Email: {email}")
    print(f"Phone: {phone}")
    
    print("\n Extracted Skills..")
    skills = extract_skills(resume_text, SKILLS_DB)
    print("Skills Found:", skills)
    
    print("Recommending Jobs...")
    recommendation = recommend_jobs(skills, JOB_DATA)
    
    print("\n Top JOb matches:")
    for job, score in recommendation:
        print(f" {job} (score: {score:.2f})")

if __name__ == "__main__":
    main()