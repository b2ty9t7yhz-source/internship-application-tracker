const applicationsList = document.querySelector("#applicationsList");
const applicationCount = document.querySelector("#applicationCount");
const refreshBtn = document.querySelector("#refreshBtn");
const applicationForm = document.querySelector("#applicationForm");
const analysisForm = document.querySelector("#analysisForm");
const analysisResult = document.querySelector("#analysisResult");
const reportForm = document.querySelector("#reportForm");
const reportResult = document.querySelector("#reportResult");

function splitCommaInput(value) {
  if (!value) return [];

  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function emptyToNull(value) {
  return value && value.trim() !== "" ? value.trim() : null;
}

function formatJson(data) {
  return JSON.stringify(data, null, 2);
}

function getStatusClass(status) {
  return status.replace(/\s+/g, "-");
}

async function apiFetch(url, options = {}) {
  const response = await fetch(url, options);

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Request failed with status ${response.status}`);
  }

  return response.json();
}

async function loadApplications() {
  applicationsList.innerHTML = "<p>Loading applications...</p>";

  try {
    const applications = await apiFetch("/applications/");

    applicationCount.textContent = `${applications.length} saved`;

    if (applications.length === 0) {
      applicationsList.innerHTML = "<p>No applications yet. Add one on the right.</p>";
      return;
    }

    applicationsList.innerHTML = applications
      .map((application) => {
        const statusClass = getStatusClass(application.status);

        return `
          <article class="application-item">
            <div class="application-top">
              <div>
                <h3 class="application-title">${application.company} — ${application.role}</h3>
                <p class="application-meta">
                  ${application.location || "Unknown location"} ·
                  ${application.source || "Unknown source"} ·
                  Resume: ${application.resume_version || "N/A"}
                </p>
                <p class="application-meta">
                  Deadline: ${application.deadline || "No deadline"}
                </p>
              </div>
              <span class="status ${statusClass}">${application.status}</span>
            </div>
          </article>
        `;
      })
      .join("");
  } catch (error) {
    applicationsList.innerHTML = `<p>Error loading applications: ${error.message}</p>`;
  }
}

applicationForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(applicationForm);

  const payload = {
    company: formData.get("company"),
    role: formData.get("role"),
    link: emptyToNull(formData.get("link")),
    type: emptyToNull(formData.get("type")),
    location: emptyToNull(formData.get("location")),
    source: emptyToNull(formData.get("source")),
    status: formData.get("status"),
    deadline: emptyToNull(formData.get("deadline")),
    date_applied: null,
    resume_version: emptyToNull(formData.get("resume_version")),
    notes: emptyToNull(formData.get("notes")),
  };

  try {
    await apiFetch("/applications/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    applicationForm.reset();
    await loadApplications();
  } catch (error) {
    alert(`Could not save application: ${error.message}`);
  }
});

analysisForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(analysisForm);

  const payload = {
    description: formData.get("description"),
    user_skills: splitCommaInput(formData.get("user_skills")),
  };

  analysisResult.textContent = "Analyzing...";

  try {
    const result = await apiFetch("/jobs/analyze-description", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    analysisResult.textContent = formatJson(result);
  } catch (error) {
    analysisResult.textContent = `Error: ${error.message}`;
  }
});

reportForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(reportForm);

  const payload = {
    company: emptyToNull(formData.get("company")),
    role: emptyToNull(formData.get("role")),
    description: formData.get("description"),
    user_skills: splitCommaInput(formData.get("user_skills")),
    deadline: emptyToNull(formData.get("deadline")),
    preferred_locations: splitCommaInput(formData.get("preferred_locations")),
    resume_versions: [
      {
        name: "resume_general_swe_v1",
        focus_area: "General SWE",
        skills: ["Python", "Java", "Git", "Data Structures"],
      },
      {
        name: "resume_backend_v1",
        focus_area: "Backend",
        skills: ["Python", "SQL", "REST API", "FastAPI", "Git", "Docker"],
      },
      {
        name: "resume_data_v1",
        focus_area: "Data",
        skills: ["Python", "SQL", "Pandas", "Machine Learning"],
      },
    ],
  };

  reportResult.innerHTML = "<p>Generating report...</p>";

  try {
    const result = await apiFetch("/reports/application-intelligence", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    renderReport(result);
  } catch (error) {
    reportResult.innerHTML = `<p>Error: ${error.message}</p>`;
  }
});

function renderReport(result) {
  const recommendedResume = result.recommended_resume
    ? result.recommended_resume.name
    : "No recommendation";

  reportResult.innerHTML = `
    <div class="report-panel">
      <h3>${result.company || "Unknown Company"} — ${result.role || "Unknown Role"}</h3>
      <div class="metric-row">
        <div class="metric">
          <strong>${result.analysis.match_score}%</strong>
          <span>Match Score</span>
        </div>
        <div class="metric">
          <strong>${result.priority.priority_score}</strong>
          <span>Priority Score</span>
        </div>
        <div class="metric">
          <strong>${result.priority.priority_level}</strong>
          <span>Priority Level</span>
        </div>
        <div class="metric">
          <strong>${recommendedResume}</strong>
          <span>Recommended Resume</span>
        </div>
      </div>
    </div>

    <div class="report-panel">
      <h3>Job Analysis</h3>
      <p><strong>Job Family:</strong> ${result.analysis.job_family}</p>
      <p><strong>Role Level:</strong> ${result.analysis.role_level}</p>
      <p><strong>Location Type:</strong> ${result.analysis.location_type}</p>
      <p><strong>Detected Skills:</strong> ${result.analysis.detected_skills.join(", ") || "None"}</p>
      <p><strong>Missing Skills:</strong> ${result.analysis.missing_skills.join(", ") || "None"}</p>
    </div>

    <div class="report-panel">
      <h3>Action Items</h3>
      <ul>
        ${result.action_items.map((item) => `<li>${item}</li>`).join("")}
      </ul>
    </div>

    <div class="report-panel">
      <h3>Suggested Notes</h3>
      <pre class="result-box">${result.suggested_notes}</pre>
    </div>
  `;
}

refreshBtn.addEventListener("click", loadApplications);

loadApplications();
