# 🚀 AI Resume Analyzer & Ranker

A full-stack NLP application that uses **Semantic Search** to match resumes to job descriptions. Unlike keyword matching, this tool understands the context of experience.

## 🧠 AI Engine
- **Model:** `all-MiniLM-L6-v2` (Sentence-Transformers)
- **Logic:** Converts text into 384-dimensional dense vectors and calculates **Cosine Similarity**.
- **Capabilities:** Can match "React Developer" to "Frontend Engineer" based on semantic meaning.

## 🛠️ Project Structure
- `/api`: FastAPI backend serving the ML model.
- `/ml_engine`: The core AI logic for extraction and matching.
- `/ui`: Streamlit frontend for a clean user experience.

## 🏃 Running the Project
1. Install: `pip install -r requirements.txt`
2. Start API: `python -m uvicorn api.main:app --reload`
3. Start UI: `streamlit run ui/app.py`