import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from ml_engine.extractor import extract_text_from_pdf
from ml_engine.matcher import analyze_resume_data

app = FastAPI(title="Resume Analyzer", description="Simple and reliable AI Resume Analyzer")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files directory
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

@app.post("/api/analyze")
async def analyze_resume(
    job_description: str = Form(None),
    job_file: UploadFile = File(None),
    resume_file: UploadFile = File(None),
    resume_text: str = Form(None)
):
    try:
        # 1. Process Job Description (either text or PDF)
        jd_text = ""
        if job_file and job_file.filename:
            file_bytes = await job_file.read()
            jd_text = extract_text_from_pdf(file_bytes)
            if jd_text.startswith("Error:"):
                return JSONResponse(
                    {"status": "error", "message": f"Job Description PDF: {jd_text}"},
                    status_code=400
                )
        elif job_description and job_description.strip():
            jd_text = job_description.strip()

        if not jd_text:
            return JSONResponse(
                {"status": "error", "message": "Please enter a Job Description or upload a Job PDF."},
                status_code=400
            )

        # 2. Process Resume (either PDF or text)
        resume_extracted = ""
        if resume_file and resume_file.filename:
            file_bytes = await resume_file.read()
            resume_extracted = extract_text_from_pdf(file_bytes)
            if resume_extracted.startswith("Error:"):
                return JSONResponse(
                    {"status": "error", "message": f"Resume PDF: {resume_extracted}"},
                    status_code=400
                )
        elif resume_text and resume_text.strip():
            resume_extracted = resume_text.strip()

        if not resume_extracted:
            return JSONResponse(
                {"status": "error", "message": "Please upload your Resume PDF or paste your resume text."},
                status_code=400
            )

        # 3. Run semantic AI analysis
        result = analyze_resume_data(jd_text, resume_extracted)

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        return JSONResponse(
            {"status": "error", "message": f"Server error: {str(e)}"},
            status_code=500
        )

# Serve index.html explicitly at root
@app.get("/")
def serve_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Resume Analyzer API is running. Add index.html to static folder."}

# Mount static folder
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

if __name__ == "__main__":
    import uvicorn
    print("Starting Resume Analyzer server at http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
