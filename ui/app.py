import streamlit as st
import os
import sys

# --- PATH FIX ---
# This ensures that the 'ui' folder can find 'ml_engine' even on a remote server
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Direct imports from your engine
from ml_engine.extractor import extract_text_from_pdf
from ml_engine.matcher import calculate_detailed_analysis # Updated Import

# Page Config
st.set_page_config(page_title="AI Resume Analyzer Pro", page_icon="📄", layout="wide")

# UI Styling
st.title("🚀 AI Resume Analyzer Pro")
st.subheader("Deep Semantic Analysis & Skill Gap Tracking")
st.markdown("---")

# Sidebar
st.sidebar.header("System Features")
st.sidebar.markdown("""
- **AI Scoring:** Semantic similarity matching.
- **Skill Extraction:** Identified matched keywords.
- **Gap Analysis:** Missing critical skills.
- **Action Plan:** Suggestions to improve rank.
""")

# User Inputs
jd_text = st.text_area(
    "Paste Job Description Here", 
    height=200, 
    placeholder="Paste the full job description here to get the most accurate skill gap analysis..."
)

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Main Logic
if st.button("Run Full Analysis"):
    if jd_text and uploaded_file:
        with st.spinner("AI is performing deep analysis..."):
            try:
                # 1. Save file temporarily
                temp_filename = "temp_web_upload.pdf"
                with open(temp_filename, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # 2. Run the Extraction
                resume_text = extract_text_from_pdf(temp_filename)
                
                if "Error" in resume_text:
                    st.error(f"Extraction Failed: {resume_text}")
                else:
                    # 3. Run the New Detailed AI Matcher
                    analysis = calculate_detailed_analysis(jd_text, resume_text)
                    score = analysis['score']
                    
                    # 4. Display results
                    st.balloons()
                    
                    # --- Header Section ---
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.metric("Overall Match Score", f"{score}%")
                    with col2:
                        if score >= 75:
                            st.success("Verdict: **Strong Match** ✅ - Your profile aligns well with this role.")
                        elif score >= 50:
                            st.warning("Verdict: **Potential Match** ⚠️ - Some key gaps identified.")
                        else:
                            st.error("Verdict: **Low Match** ❌ - Significant skill gaps detected.")

                    st.divider()

                    # --- New Features: Detailed Analysis ---
                    tab1, tab2, tab3 = st.tabs(["🌟 Key Highlights", "🚩 Skill Gaps", "💡 Action Plan"])

                    with tab1:
                        st.write("### Matched Skills")
                        if analysis['matched']:
                            # Display matched skills as colorful tags
                            skills_html = "".join([f'<span style="background-color:#d4edda; color:#155724; padding:5px 10px; margin:5px; border-radius:15px; display:inline-block; font-weight:bold;">{s}</span>' for s in analysis['matched']])
                            st.markdown(skills_html, unsafe_allow_stdio=True)
                        else:
                            st.write("No direct skill matches found. Consider using industry-standard terminology.")

                    with tab2:
                        st.write("### Missing Skills")
                        if analysis['missing']:
                            st.write("The following keywords were found in the Job Description but not in your resume:")
                            missing_html = "".join([f'<span style="background-color:#f8d7da; color:#721c24; padding:5px 10px; margin:5px; border-radius:15px; display:inline-block; font-weight:bold;">{s}</span>' for s in analysis['missing']])
                            st.markdown(missing_html, unsafe_allow_stdio=True)
                        else:
                            st.write("🎉 No major skill gaps found!")

                    with tab3:
                        st.write("### How to improve your score")
                        for suggestion in analysis['suggestions']:
                            st.info(f"👉 {suggestion}")

                # 5. Clean up the temporary file
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please provide both a Job Description and a Resume PDF.")

st.markdown("---")
st.caption("Developed by [Your Name] | Logic: Semantic Similarity + Keyword Extraction")