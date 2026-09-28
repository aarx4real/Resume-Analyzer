# Resume Analyzer

A simple web application to check how well a resume matches a job description using AI.

## Features
- **Upload Resume**: Upload your resume in PDF format (or paste resume text).
- **Enter Job Description**: Paste the job description text or upload a job PDF.
- **Match Score**: Get an overall match percentage score.
- **Skill Breakdown**: See which skills match and which important skills are missing.
- **Actionable Tips**: Get practical suggestions to improve your resume for the role.

## Technologies Used
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (located in `static/`)
- **Backend**: Python, FastAPI (`app.py`)
- **AI / NLP**: `sentence-transformers` (`all-MiniLM-L6-v2`) for semantic similarity and PyMuPDF for PDF text extraction.

## How to Run Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aarx4real/Resume-Analyzer.git
   cd Resume-Analyzer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server**:
   ```bash
   python app.py
   ```