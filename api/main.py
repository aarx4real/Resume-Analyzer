import sys
import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form

# --- PATH FIX ---
# This ensures that the 'api' folder can find the 'ml_engine' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_engine.extractor import extract_text_from_pdf
from ml_engine.matcher import calculate_similarity # New Import!

app = FastAPI(
    title="Resume Analyzer AI",
    description="Professional API for resume screening and job matching",
    version="1.0.0"
)

# Ensure a temporary directory exists for uploads
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {
        "message": "Resume Analyzer API is Online",
        "docs_url": "/docs"
    }

@app.post("/extract-text/")
async def upload_resume(file: UploadFile = File(...)):
    """
    Endpoint to extract raw text from a PDF resume.
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        extracted_text = extract_text_from_pdf(file_path)
        
        return {
            "filename": file.filename,
            "text_length": len(extracted_text),
            "content_preview": extracted_text[:500] 
        }
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@app.post("/analyze-resume/")
async def analyze_resume(
    job_description: str = Form(...), 
    file: UploadFile = File(...)
):
    """
    Takes a Job Description AND a Resume, extracts text, 
    and returns a semantic match score using AI.
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        # 1. Save file locally
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Extract text from PDF
        resume_text = extract_text_from_pdf(file_path)
        
        # 3. Calculate Semantic Similarity Score (AI Logic)
        match_score = calculate_similarity(job_description, resume_text)
        
        # 4. Generate a simple verdict
        verdict = "Strong Match" if match_score > 75 else "Potential Match" if match_score > 50 else "Low Match"
        
        return {
            "status": "Success",
            "resume_filename": file.filename,
            "match_score": f"{match_score}%",
            "verdict": verdict,
            "job_desc_preview": f"{job_description[:100]}..."
        }
        
    except Exception as e:
        return {"status": "Error", "message": str(e)}
        
    finally:
        # Cleanup: Remove file from server after processing
        if os.path.exists(file_path):
            os.remove(file_path)