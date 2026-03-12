import streamlit as st
import os
import sys

# --- PATH FIX ---
# This ensures that the 'ui' folder can find 'ml_engine' even on a remote server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Direct imports from your engine instead of calling a local API
from ml_engine.extractor import extract_text_from_pdf
from ml_engine.matcher import calculate_similarity

# Page Config
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")

# UI Styling
st.title("🚀 AI Resume Analyzer")
st.subheader("Get an instant AI match score based on your skills")
st.markdown("---")

# Sidebar
st.sidebar.header("About")
st.sidebar.info(
    "This tool uses Natural Language Processing (NLP) to compare resumes "
    "to job descriptions using semantic similarity."
)

# User Inputs
jd_text = st.text_area(
    "Paste Job Description Here", 
    height=200, 
    placeholder="e.g., We are looking for a Python Developer with experience in FastAPI and Machine Learning..."
)

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Main Logic
if st.button("Analyze Match"):
    if jd_text and uploaded_file:
        with st.spinner("AI is analyzing the semantic match..."):
            try:
                # 1. Save file temporarily (required for the PDF extractor)
                temp_filename = "temp_web_upload.pdf"
                with open(temp_filename, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # 2. Run the Extraction
                resume_text = extract_text_from_pdf(temp_filename)
                
                if "Error" in resume_text:
                    st.error(f"Extraction Failed: {resume_text}")
                else:
                    # 3. Run the AI Matcher
                    score = calculate_similarity(jd_text, resume_text)
                    
                    # 4. Display results
                    st.balloons()
                    st.divider()
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Match Score", f"{score}%")
                    
                    # Logic for the Verdict
                    if score >= 75:
                        col2.success("Verdict: **Strong Match** ✅")
                    elif score >= 50:
                        col2.warning("Verdict: **Potential Match** ⚠️")
                    else:
                        col2.error("Verdict: **Low Match** ❌")
                        
                    st.info("The score is based on how well the meanings of your experiences align with the job requirements.")

                # 5. Clean up the temporary file
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please provide both a Job Description and a Resume PDF.")

st.markdown("---")
st.caption("Developed by [Your Name] | Powered by Sentence-Transformers (MiniLM)")