from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommend_jobs(candidate_skills: list, job_data: dict, top_n: int = 3) -> list:
    """
    candidate_skills : list of extracted skills
    job_data         : dict {job_title: job_description}
    top_n            : number of recommendations
    """

    if not candidate_skills:
        return []

    candidate_text = " ".join(candidate_skills)

    documents = [candidate_text] + list(job_data.values())

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_scores = cosine_similarity(
        tfidf_matrix[0:1], tfidf_matrix[1:]
    ).flatten()

    job_scores = list(zip(job_data.keys(), similarity_scores))

    job_scores = sorted(job_scores, key=lambda x: x[1], reverse=True)

    return job_scores[:top_n]


# =========================
# TESTING
# =========================
if __name__ == "__main__":

    candidate_skills = [
        "Python", "Machine Learning", "SQL", "Pandas", "Deep Learning", "TensorFlow"
    ]

    job_data = {
        "Data Scientist": "Python Machine Learning SQL Pandas Statistics",
        "Machine Learning Engineer": "Python Machine Learning Deep Learning TensorFlow PyTorch",
        "Data Analyst": "Python SQL Excel Data Analysis Visualization",
        "AI Engineer": "Python Deep Learning TensorFlow PyTorch NLP",
        "Backend Developer": "Python Django REST API SQL"
    }

    recommendations = recommend_jobs(candidate_skills, job_data)

    print("Recommended Jobs:")
    for job, score in recommendations:
        print(f"{job} → Match: {int(score * 100)}%")
