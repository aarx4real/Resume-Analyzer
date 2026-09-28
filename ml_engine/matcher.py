import os
import re
import json
import requests
from sentence_transformers import SentenceTransformer, util

# Load the semantic model locally
model = SentenceTransformer('all-MiniLM-L6-v2')

# A comprehensive list of skills for the analyzer to "look for"
SKILL_DB = [
    # Languages
    "Python", "Java", "C++", "C#", "C", "JavaScript", "TypeScript", "HTML", "CSS", "SQL", "PHP", "Ruby", "Go", "Rust", "Swift", "Kotlin",
    # Frameworks & Libraries
    "React", "Angular", "Vue", "Next.js", "Node.js", "Express", "FastAPI", "Flask", "Django", "Spring Boot", ".NET",
    # Databases & Cloud
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Firebase", "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Linux",
    # AI / ML / Data
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "Data Science", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Data Analysis", "Tableau", "Power BI",
    # Tools & Methodologies
    "Git", "GitHub", "GitLab", "CI/CD", "REST API", "GraphQL", "Agile", "Scrum", "Jira", "Excel", "Project Management", "Communication", "Problem Solving"
]

def extract_skills(text: str):
    """
    Scans the text for keywords defined in SKILL_DB using regex.
    """
    found_skills = set()
    for skill in SKILL_DB:
        # Match whole word, case-insensitive
        pattern = rf"\b{re.escape(skill)}\b"
        if re.search(pattern, text, re.IGNORECASE):
            found_skills.add(skill)
    return found_skills

def calculate_detailed_analysis(job_description: str, resume_text: str):
    """
    Performs a dual-layer local analysis: Semantic embeddings + Keyword matching.
    """
    # 1. Semantic Similarity (all-MiniLM-L6-v2)
    embeddings1 = model.encode(job_description, convert_to_tensor=True)
    embeddings2 = model.encode(resume_text, convert_to_tensor=True)
    cosine_score = util.cos_sim(embeddings1, embeddings2)
    semantic_score = round(float(cosine_score[0][0]) * 100, 1)

    # Clamp between 0 and 100
    semantic_score = max(0.0, min(100.0, semantic_score))

    # 2. Keyword/Skill Extraction
    jd_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)

    # 3. Gap Analysis
    matched_skills = sorted(list(jd_skills.intersection(resume_skills)))
    missing_skills = sorted(list(jd_skills.difference(resume_skills)))

    # 4. Generate Suggestions
    suggestions = []
    if missing_skills:
        for skill in missing_skills[:4]:
            suggestions.append(f"Highlight experience with '{skill}' or add relevant projects covering it.")
    else:
        suggestions.append("Your skills match all key technical requirements extracted from the job description!")

    if semantic_score < 60 and matched_skills:
        suggestions.append("Align your project descriptions and bullet points closer to the language used in the job post.")
    elif semantic_score >= 80:
        suggestions.append("Strong semantic overlap! Emphasize measurable achievements and metrics in your interview prep.")

    verdict = "Strong Match" if semantic_score >= 75 else "Potential Match" if semantic_score >= 50 else "Low Match"

    return {
        "score": semantic_score,
        "verdict": verdict,
        "matched": matched_skills,
        "missing": missing_skills,
        "suggestions": suggestions,
        "summary": "Analyzed using local semantic neural embeddings (all-MiniLM-L6-v2) and skill extraction.",
        "engine": "Local Fast AI (Sentence-Transformers)"
    }

def analyze_with_gemini(job_description: str, resume_text: str, api_key: str):
    """
    Calls Google Gemini API (gemini-1.5-flash or gemini-2.5-flash) to evaluate resume fit.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = f"""You are an expert technical recruiter and resume analyzer.
Compare the following Resume to the Job Description and return a JSON object ONLY with the following structure:
{{
  "score": <number between 0 and 100 representing realistic percentage match>,
  "verdict": "<Strong Match | Potential Match | Low Match>",
  "matched": [<list of strings of skills/qualifications present in both>],
  "missing": [<list of strings of important required skills from JD missing in resume>],
  "suggestions": [<3 to 5 actionable, clear suggestions to improve resume for this role>],
  "summary": "<2-3 sentence clear summary of candidate fit>"
}}

JOB DESCRIPTION:
{job_description[:3000]}

RESUME TEXT:
{resume_text[:4000]}

Return valid JSON only. Do not include markdown code block backticks if possible, or format as clean JSON.
"""

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.2
        }
    }

    response = requests.post(url, headers=headers, json=payload, timeout=12)
    response.raise_for_status()
    data = response.json()

    raw_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
    
    # Strip markdown backticks if present
    if raw_text.startswith("```"):
        raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
        raw_text = re.sub(r"\s*```$", "", raw_text)

    parsed = json.loads(raw_text)
    parsed["engine"] = "Google Gemini AI"
    return parsed

def analyze_resume_data(job_description: str, resume_text: str, api_key: str = None):
    """
    Main analysis pipeline:
    Tries Gemini API if a key is provided or found in environment,
    otherwise instantly falls back to local fast NLP engine.
    """
    key_to_use = (api_key or "").strip() or os.environ.get("GEMINI_API_KEY", "").strip()

    if key_to_use:
        try:
            return analyze_with_gemini(job_description, resume_text, key_to_use)
        except Exception:
            # If API key call fails (invalid key, rate limit, network), fall back seamlessly to local
            result = calculate_detailed_analysis(job_description, resume_text)
            result["note"] = "External API call failed; automatically used local AI model."
            return result

    # Default to fast, reliable local model
    return calculate_detailed_analysis(job_description, resume_text)

def calculate_similarity(job_description: str, resume_text: str) -> float:
    """
    Computes and returns the semantic similarity score between job description and resume.
    """
    analysis = calculate_detailed_analysis(job_description, resume_text)
    return analysis["score"]
