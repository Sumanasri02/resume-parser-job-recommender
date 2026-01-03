from sklearn.feature_extraction.text import TfidfVectorizer #text ->  numerical vectore
from sklearn.metrics.pairwise import cosine_similarity # measure how similar 2 vectors are

def recommend_jobs(candidate_skills: list, job_date: dict, top_n: int = 3) -> list:
    candidate_text = " ".join(candidate_skills) # candidate skills -> one string
    documents = [candidate_text] + list(job_date.values()) # + resume text + job description
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # calculate cosine similarity  --> angle similarity -> 1 -perfect and 0 - no match
    # tfidf_matric[0:1] --> candidate vs tfidf_matrix[1:] --> jobs
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    # Map scores to job titles
    #[("Data Scientist", 0.68),("Machine Learning Engineer", 0.82),...]
    job_scores = list(zip(job_date.keys(), similarity_scores))
    
    # sort jobs by similarity score
    job_scores = sorted(job_scores, key=lambda x: x[1], reverse=True)
    
    # return top N job titles
    recommend_jobs = job_scores[:top_n]
    
    return recommend_jobs

if __name__ == "__main__":
    
    candidate_skills = [
        "Python", "Machine Learning", "SQL", "Pandas", "Deep Learning", "TensorFlow"
    ]
    
    # HR job DB
    job_data = {
        "Data Scientist": "Python Machine Learning SQL Pandas Statistics",
        "Machine Learning Engineer": "Python Machine Learning Deep Learning TensorFlow PyTorch",
        "Data Analyst": "Python SQL Excel Data Analysis Visualization",
        "AI Engineer": "Python Deep Learning TensorFlow PyTorch NLP",
        "Backend Developer": "Python Django REST API SQL"
    }
    
    recommendations = recommend_jobs(candidate_skills, job_data)
    
    print("Recommended jobs:")
    for job, score in recommendations:
        print(f"{job} -> Similarity Score: {score:.2f}")
    