import re 
import spacy # NLP library, used to tokenize text, detect nouns/proper nouns and prepare for skill matching
nlp = spacy.load("en_core_web_sm")
# loads the small english model, texts --> tokens, identify the POS, Stopwords
SKILLS_SYNONYMS = {
    "py": "Python",
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "tf": "TensorFlow",
    "pt": "PyTorch",
} # abbreviation: py,ml. dictionary normalizes --> standard

def extract_skills(text: str, skill_database: list) -> list:
    #text -> raw text, skill_database -> list of known skills, return -> list of detected skills
    text_lower = text.lower() # text -> lowercase
    doc = nlp(text_lower) # tokenized representation
    candidate_tokens = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN", "VERB"]]
    #token--skills or technical terms, stopword ignore
    detected_skills = [] # store skills that match the DB
    
    # match each skills from DB
    for skill in skill_database:
        skill_lower = skill.lower()
        if skill_lower in text_lower or skill_lower in candidate_tokens:
            normalized_skill = SKILLS_SYNONYMS.get(skill_lower, skill)
            detected_skills.append(normalized_skill)
    detected_skills = list(set(detected_skills))
        # list -> set -> list, no duplicate skill
    return detected_skills
    
if __name__ == "__main__":
    sample_text = """
    I have worked extensively in Python, pandas, SQL, Machine Learning, and Deep Learning.
    Also familiar with TensorFlow and PyTorch.
    """
    skills_db = ["Python", "Machine Learning", "SQL", "Pandas", "Excel", "Deep Learning", "TensorFlow", "PyTorch"]
    
    extracted_skills = extract_skills(sample_text, skills_db)
    print("Skills Extracted:", extracted_skills)
    
        
    
    