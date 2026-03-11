import streamlit as st
import requests

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("🚀 AI Resume Analyzer")
st.subheader("Upload your resume and get an instant AI match score")

# Sidebar for API Status
st.sidebar.header("System Status")
try:
    response = requests.get("http://127.0.0.1:8000/")
    if response.status_code == 200:
        st.sidebar.success("Backend API: Online")
except:
    st.sidebar.error("Backend API: Offline")

# Inputs
jd_text = st.text_area("Paste Job Description Here", height=200)
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if st.button("Analyze Resume"):
    if jd_text and uploaded_file:
        with st.spinner("AI is thinking..."):
            # Prepare the data for our API
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            data = {"job_description": jd_text}
            
            # Send to our FastAPI backend
            res = requests.post("http://127.0.0.1:8000/analyze-resume/", data=data, files=files)
            
            if res.status_code == 200:
                result = res.json()
                st.balloons()
                st.metric(label="Match Score", value=result["match_score"])
                st.write(f"**Verdict:** {result['verdict']}")
            else:
                st.error("Error connecting to the AI brain.")
    else:
        st.warning("Please provide both a Job Description and a Resume.")