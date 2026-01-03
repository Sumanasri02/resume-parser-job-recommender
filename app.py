import streamlit as st
import tempfile
import os

from src.resume_parser import extract_text_from_pdf, extract_email, extract_phone
from src.skill_extractor import extract_skills
from src.job_recommender import recommend_jobs


# =========================
# UI STYLING (Professional)
# =========================
st.markdown("""
<style>
    body {
        background-color: #F7F9FC;
        color: #2C2C2C;
    }

    h1, h2, h3 {
        color: #1F3C88;
    }

    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1F3C88;
        margin-bottom: 10px;
    }

    .stButton > button {
        background-color: #1ABC9C;
        color: white;
        border-radius: 6px;
        padding: 0.6em 1.2em;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #17A589;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# DATA
# =========================
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


# =========================
# HEADER
# =========================
st.markdown("""
<div class="card" style="text-align:center;">
    <h1>📄 Resume Parser & Job Recommender</h1>
    <p style="color:#555;">
        AI-powered resume analysis for HR & recruitment teams
    </p>
</div>
""", unsafe_allow_html=True)


# =========================
# UPLOAD SECTION
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📤 Upload Resume (PDF)</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a resume file", type=["pdf"])
st.markdown('</div>', unsafe_allow_html=True)


# =========================
# ANALYZE BUTTON
# =========================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze = st.button("🔍 Analyze Resume")


# =========================
# PROCESSING
# =========================
if uploaded_file and analyze:
    with st.spinner("Analyzing resume..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name

        resume_text = extract_text_from_pdf(temp_path)
        email = extract_email(resume_text)
        phone = extract_phone(resume_text)
        skills = extract_skills(resume_text, SKILLS_DB)
        recommendations = recommend_jobs(skills, JOB_DATA)

        os.remove(temp_path)


    # =========================
    # CONTACT INFO
    # =========================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📧 Contact Information</div>', unsafe_allow_html=True)
    st.write(f"**Email:** {email if email else 'Not found'}")
    st.write(f"**Phone:** {phone if phone else 'Not found'}")
    st.markdown('</div>', unsafe_allow_html=True)


    # =========================
    # SKILLS
    # =========================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧠 Extracted Skills</div>', unsafe_allow_html=True)

    if skills:
        st.write(", ".join(skills))
    else:
        st.warning("No skills detected")

    st.markdown('</div>', unsafe_allow_html=True)


    # =========================
    # JOB RECOMMENDATIONS
    # =========================
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💼 Recommended Job Roles</div>', unsafe_allow_html=True)

    for job, score in recommendations:
        st.write(f"✅ **{job}** — Similarity Score: `{score:.2f}`")

    st.markdown('</div>', unsafe_allow_html=True)
