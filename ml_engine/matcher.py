from sentence_transformers import SentenceTransformer, util
import re

# Load the semantic model
model = SentenceTransformer('all-MiniLM-L6-v2')

# A comprehensive list of skills for the analyzer to "look for"
# You can expand this list as needed
SKILL_DB = [
    "Python", "Java", "C++", "JavaScript", "TypeScript", "React", "Angular", "Vue",
    "Node.js", "FastAPI", "Flask", "Django", "SQL", "NoSQL", "MongoDB", "PostgreSQL",
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Jenkins",
    "Machine Learning", "Deep Learning", "NLP", "Data Science", "Pandas", "NumPy",
    "Scikit-learn", "TensorFlow", "PyTorch", "Data Analysis", "Project Management",
    "Agile", "Scrum", "Communication", "Leadership", "Git", "GitHub", "Excel"
]

def extract_skills(text: str):
    """
    Scans the text for keywords defined in SKILL_DB using regex.
    """
    found_skills = set()
    for skill in SKILL_DB:
        # \b ensures we match the whole word (e.g., 'Java' doesn't match 'JavaScript')
        pattern = rf"\b{re.escape(skill)}\b"
        if re.search(pattern, text, re.IGNORECASE):
            found_skills.add(skill)
    return found_skills

def calculate_detailed_analysis(job_description: str, resume_text: str):
    """
    Performs a dual-layer analysis: Semantic meaning + Keyword matching.
    """
    # 1. Semantic Similarity (The 'AI' Score)
    embeddings1 = model.encode(job_description, convert_to_tensor=True)
    embeddings2 = model.encode(resume_text, convert_to_tensor=True)
    cosine_score = util.cos_sim(embeddings1, embeddings2)
    semantic_score = round(float(cosine_score[0][0]) * 100, 2)

    # 2. Keyword/Skill Extraction
    jd_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)

    # 3. Gap Analysis
    matched_skills = jd_skills.intersection(resume_skills)
    missing_skills = jd_skills.difference(resume_skills)

    # 4. Generate Smart Suggestions
    suggestions = []
    if missing_skills:
        # Suggest the first 3 missing skills
        for skill in list(missing_skills)[:3]:
            suggestions.append(f"Consider adding '{skill}' to your resume if you have experience with it.")
    else:
        suggestions.append("Your skill set aligns perfectly with the job description keywords!")

    # If the score is low but skills match, give specific advice
    if semantic_score < 60 and matched_skills:
        suggestions.append("Try rewriting your experience bullet points to mirror the language used in the job description.")

    return {
        "score": semantic_score,
        "matched": list(matched_skills),
        "missing": list(missing_skills),
        "suggestions": suggestions
    }