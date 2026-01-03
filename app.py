import streamlit as st
import tempfile
import os
import pandas as pd
import logging

# 🔕 Suppress Streamlit warning logs
logging.getLogger("streamlit.runtime.scriptrunner").setLevel(logging.ERROR)

from src.resume_parser import extract_text_from_pdf, extract_email, extract_phone
from src.skill_extractor import extract_skills
from src.job_recommender import recommend_jobs


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Resume Parser & Job Recommender",
    layout="wide"
)

# =========================
# UI STYLING
# =========================
st.markdown("""
<style>
    body { background-color: #F7F9FC; }
    .card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 18px;
        font-weight: 600;
        color: #1F3C88;
        margin-bottom: 10px;
    }
    .stButton > button {
        background-color: #1ABC9C;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        padding: 8px 20px;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# DATA
# =========================
SKILLS_DB = [
    # Programming
    "Python", "Java", "C++", "JavaScript",

    # Web
    "HTML", "CSS", "React", "Node.js",

    # Backend
    "Django", "Flask", "FastAPI", "REST API",

    # Databases
    "SQL", "MySQL", "PostgreSQL", "MongoDB",

    # Data & AI
    "Pandas", "NumPy", "Machine Learning", "Deep Learning",
    "NLP", "Computer Vision", "Data Analysis",

    # Frameworks
    "TensorFlow", "PyTorch", "Scikit-learn",

    # Cloud & DevOps
    "AWS", "Azure", "Docker", "Kubernetes", "CI/CD",

    # Visualization
    "Power BI", "Tableau", "Matplotlib", "Seaborn",

    # Soft Skills
    "Communication", "Leadership", "Problem Solving"
]


JOB_DATA = {
    "Data Scientist":
        "Python Machine Learning SQL Pandas Statistics NLP",

    "Machine Learning Engineer":
        "Python Machine Learning Deep Learning TensorFlow PyTorch Docker",

    "Data Analyst":
        "Python SQL Excel Power BI Tableau Data Analysis",

    "AI Engineer":
        "Python Deep Learning NLP Computer Vision TensorFlow PyTorch",

    "Backend Developer":
        "Python Django FastAPI REST API SQL Docker",

    "Full Stack Developer":
        "JavaScript React Node.js MongoDB SQL HTML CSS",

    "Software Engineer":
        "Python Java C++ Data Structures Algorithms",

    "DevOps Engineer":
        "AWS Docker Kubernetes CI/CD Linux",

    "Cloud Engineer":
        "AWS Azure GCP Docker Kubernetes",

    "Business Analyst":
        "Excel SQL Power BI Communication Analysis"
}



# =========================
# HEADER
# =========================
st.markdown("""
<div class="card" style="text-align:center;">
    <h1>📄 Resume Parser & Job Recommender</h1>
    <p>Upload resumes and automatically get skill extraction & job recommendations</p>
</div>
""", unsafe_allow_html=True)


# =========================
# FILE UPLOAD
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📤 Upload Resume PDFs</div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload one or more resumes",
    type=["pdf"],
    accept_multiple_files=True
)

st.markdown('</div>', unsafe_allow_html=True)


# =========================
# ANALYZE BUTTON
# =========================
analyze = st.button("🔍 Analyze Resumes")


# =========================
# PROCESSING
# =========================
if analyze and uploaded_files:
    results = []

    with st.spinner("Analyzing resumes automatically..."):
        for file in uploaded_files:

            # Save PDF temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file.read())
                temp_path = tmp.name

            # Resume processing
            resume_text = extract_text_from_pdf(temp_path)
            email = extract_email(resume_text)
            phone = extract_phone(resume_text)
            skills = extract_skills(resume_text, SKILLS_DB)
            recommendations = recommend_jobs(skills, JOB_DATA)

            os.remove(temp_path)

            results.append({
                "Resume": file.name,
                "Email": email if email else "Not found",
                "Phone": phone if phone else "Not found",
                "Skills": ", ".join(skills) if skills else "None",
                "Top Job Match": recommendations[0][0] if recommendations else "None"
            })

    # =========================
    # RESULTS TABLE
    # =========================
    df = pd.DataFrame(results)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Parsed Resume Results</div>', unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # DOWNLOAD CSV
    # =========================
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Download Results as CSV",
        csv,
        "resume_analysis_results.csv",
        "text/csv"
    )
