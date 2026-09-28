// Resume Analyzer Frontend Logic
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("analyze-form");
    const submitBtn = document.getElementById("submit-btn");
    const sampleBtn = document.getElementById("sample-btn");
    const loadingDiv = document.getElementById("loading");
    const errorDiv = document.getElementById("error-message");
    const resultsSection = document.getElementById("results");

    const scoreValue = document.getElementById("score-value");
    const verdictBadge = document.getElementById("verdict-badge");
    const progressBar = document.getElementById("progress-bar");
    const summaryText = document.getElementById("summary-text");
    const matchedSkillsDiv = document.getElementById("matched-skills");
    const missingSkillsDiv = document.getElementById("missing-skills");
    const suggestionsList = document.getElementById("suggestions-list");

    const jdInput = document.getElementById("job-description");
    const jobFileInput = document.getElementById("job-file");
    const resumeFileInput = document.getElementById("resume-file");
    const resumeTextInput = document.getElementById("resume-text");

    // Load Sample Data Helper
    sampleBtn.addEventListener("click", () => {
        jdInput.value = `Senior Full Stack Developer
Requirements:
- 3+ years of experience with Python, FastAPI, and PostgreSQL
- Strong skills in React, TypeScript, HTML, CSS, and modern JavaScript
- Experience with Docker, Git, CI/CD, and REST APIs
- Familiarity with Cloud platforms (AWS or GCP)
- Good problem solving and communication skills`;

        resumeTextInput.value = `John Doe
Full Stack Software Developer

Technical Skills:
- Languages: Python, JavaScript, HTML, CSS, SQL
- Frameworks: FastAPI, Django, React, Node.js
- Tools: Git, GitHub, Docker, Linux, MySQL
- Other: REST API development, Agile methodologies

Experience:
Software Engineer at TechCorp
- Built scalable web applications with Python and FastAPI backend.
- Designed responsive user interfaces using React and JavaScript.
- Managed relational database schemas and queries in MySQL.
- Automated code testing and deployments using Git and Docker.`;

        resumeFileInput.value = "";
        jobFileInput.value = "";
        hideError();
    });

    // Form Submit Handler
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        hideError();

        const jdText = jdInput.value.trim();
        const jobFile = jobFileInput.files[0];
        const resumeFile = resumeFileInput.files[0];
        const resumeText = resumeTextInput.value.trim();

        if (!resumeFile && !resumeText) {
            showError("Please upload your Resume PDF or paste your resume text.");
            return;
        }

        if (!jdText && !jobFile) {
            showError("Please enter a Job Description or upload a Job PDF.");
            return;
        }

        // Prepare FormData
        const formData = new FormData();
        if (resumeFile) {
            formData.append("resume_file", resumeFile);
        }
        if (resumeText) {
            formData.append("resume_text", resumeText);
        }
        if (jdText) {
            formData.append("job_description", jdText);
        }
        if (jobFile) {
            formData.append("job_file", jobFile);
        }

        // UI Loading State
        submitBtn.disabled = true;
        submitBtn.textContent = "Analyzing...";
        loadingDiv.classList.remove("hidden");
        resultsSection.classList.add("hidden");

        try {
            const response = await fetch("/api/analyze", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();

            if (!response.ok || data.status !== "success") {
                throw new Error(data.message || "Failed to analyze resume.");
            }

            renderResults(data.data);
            resultsSection.scrollIntoView({ behavior: "smooth" });

        } catch (err) {
            showError(err.message || "Something went wrong. Please check your inputs and try again.");
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = "Analyze Resume";
            loadingDiv.classList.add("hidden");
        }
    });

    // Render Analysis Results
    function renderResults(data) {
        const score = Math.round(data.score || 0);
        const verdict = data.verdict || "Match Evaluated";

        scoreValue.textContent = `${score}%`;
        progressBar.style.width = `${score}%`;
        verdictBadge.textContent = verdict;

        // Color coding for verdict badge
        verdictBadge.className = "verdict-badge";
        if (score >= 75) {
            verdictBadge.classList.add("verdict-strong");
            progressBar.style.backgroundColor = "#38a169";
        } else if (score >= 50) {
            verdictBadge.classList.add("verdict-potential");
            progressBar.style.backgroundColor = "#dd6b20";
        } else {
            verdictBadge.classList.add("verdict-low");
            progressBar.style.backgroundColor = "#e53e3e";
        }

        // Summary
        summaryText.textContent = data.summary || "No summary provided.";

        // Matched Skills
        matchedSkillsDiv.innerHTML = "";
        const matched = data.matched || [];
        if (matched.length > 0) {
            matched.forEach((skill) => {
                const span = document.createElement("span");
                span.className = "tag tag-matched";
                span.textContent = skill;
                matchedSkillsDiv.appendChild(span);
            });
        } else {
            matchedSkillsDiv.innerHTML = `<span class="empty-text">No direct skills matched.</span>`;
        }

        // Missing Skills
        missingSkillsDiv.innerHTML = "";
        const missing = data.missing || [];
        if (missing.length > 0) {
            missing.forEach((skill) => {
                const span = document.createElement("span");
                span.className = "tag tag-missing";
                span.textContent = skill;
                missingSkillsDiv.appendChild(span);
            });
        } else {
            missingSkillsDiv.innerHTML = `<span class="empty-text">No critical missing skills detected!</span>`;
        }

        // Suggestions
        suggestionsList.innerHTML = "";
        const suggestions = data.suggestions || [];
        if (suggestions.length > 0) {
            suggestions.forEach((tip) => {
                const li = document.createElement("li");
                li.textContent = tip;
                suggestionsList.appendChild(li);
            });
        } else {
            const li = document.createElement("li");
            li.textContent = "Your resume is well aligned with the job description.";
            suggestionsList.appendChild(li);
        }

        resultsSection.classList.remove("hidden");
    }

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.classList.remove("hidden");
    }

    function hideError() {
        errorDiv.textContent = "";
        errorDiv.classList.add("hidden");
    }
});
