const applicationsList = document.querySelector("#applicationsList");
const applicationCount = document.querySelector("#applicationCount");
const refreshBtn = document.querySelector("#refreshBtn");
const applicationForm = document.querySelector("#applicationForm");
const importForm = document.querySelector("#importForm");
const importResult = document.querySelector("#importResult");
const analysisForm = document.querySelector("#analysisForm");
const analysisResult = document.querySelector("#analysisResult");
const reportForm = document.querySelector("#reportForm");
const reportResult = document.querySelector("#reportResult");

const totalApplications = document.querySelector("#totalApplications");
const savedApplications = document.querySelector("#savedApplications");
const appliedApplications = document.querySelector("#appliedApplications");
const interviewApplications = document.querySelector("#interviewApplications");
const upcomingDeadlines = document.querySelector("#upcomingDeadlines");
const lastUpdated = document.querySelector("#lastUpdated");

const STATUSES = ["Saved", "Applied", "OA", "Interview", "Rejected", "Offer", "No Response"];

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

function escapeHtml(value) {
  if (value === null || value === undefined) return "";

  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
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

async function loadDashboard() {
  try {
    const summary = await apiFetch("/stats/summary");

    totalApplications.textContent = summary.total_applications ?? 0;
    savedApplications.textContent = summary.saved ?? 0;
    appliedApplications.textContent = summary.applied ?? 0;
    interviewApplications.textContent = summary.interview ?? 0;
    upcomingDeadlines.textContent = summary.upcoming_deadlines_next_14_days ?? 0;
    lastUpdated.textContent = `Updated ${new Date().toLocaleTimeString()}`;
  } catch (error) {
    lastUpdated.textContent = `Dashboard error: ${error.message}`;
  }
}

async function loadApplications() {
  applicationsList.innerHTML = "<p>Loading applications...</p>";

  try {
    const applications = await apiFetch("/applications/");

    applicationCount.textContent = `${applications.length} saved`;

    if (applications.length === 0) {
      applicationsList.innerHTML = "<p>No applications yet. Add or import one.</p>";
      return;
    }

    applicationsList.innerHTML = applications
      .map((application) => renderApplication(application))
      .join("");

    document.querySelectorAll("[data-status-select]").forEach((select) => {
      select.addEventListener("change", async (event) => {
        const id = event.target.dataset.id;
        const status = event.target.value;
        await updateApplicationStatus(id, status);
      });
    });

    document.querySelectorAll("[data-delete-button]").forEach((button) => {
      button.addEventListener("click", async (event) => {
        const id = event.target.dataset.id;
        await deleteApplication(id);
      });
    });
  } catch (error) {
    applicationsList.innerHTML = `<p>Error loading applications: ${escapeHtml(error.message)}</p>`;
  }
}

function renderApplication(application) {
  const statusClass = getStatusClass(application.status);

  const statusOptions = STATUSES.map((status) => {
    const selected = status === application.status ? "selected" : "";
    return `<option ${selected}>${status}</option>`;
  }).join("");

  return `
    <article class="application-item">
      <div class="application-top">
        <div>
          <h3 class="application-title">
            ${escapeHtml(application.company)} — ${escapeHtml(application.role)}
          </h3>
          <p class="application-meta">
            ${escapeHtml(application.location || "Unknown location")} ·
            ${escapeHtml(application.source || "Unknown source")} ·
            Resume: ${escapeHtml(application.resume_version || "N/A")}
          </p>
          <p class="application-meta">
            Deadline: ${escapeHtml(application.deadline || "No deadline")}
          </p>
          ${
            application.link
              ? `<p class="application-meta"><a href="${escapeHtml(application.link)}" target="_blank">Open job link</a></p>`
              : ""
          }
        </div>
        <span class="status ${statusClass}">${escapeHtml(application.status)}</span>
      </div>

      <div class="application-actions">
        <select data-status-select data-id="${application.id}">
          ${statusOptions}
        </select>
        <button class="danger" data-delete-button data-id="${application.id}">Delete</button>
      </div>
    </article>
  `;
}

async function updateApplicationStatus(id, status) {
  try {
    await apiFetch(`/applications/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ status }),
    });

    await refreshAll();
  } catch (error) {
    alert(`Could not update status: ${error.message}`);
  }
}

async function deleteApplication(id) {
  const confirmed = window.confirm("Delete this application?");
  if (!confirmed) return;

  try {
    await apiFetch(`/applications/${id}`, {
      method: "DELETE",
    });

    await refreshAll();
  } catch (error) {
    alert(`Could not delete application: ${error.message}`);
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
    await refreshAll();
  } catch (error) {
    alert(`Could not save application: ${error.message}`);
  }
});

importForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(importForm);

  const payload = {
    company: formData.get("company"),
    role: formData.get("role"),
    description: formData.get("description"),
    link: emptyToNull(formData.get("link")),
    source: emptyToNull(formData.get("source")) || "Manual Import",
    resume_version: emptyToNull(formData.get("resume_version")),
    user_skills: splitCommaInput(formData.get("user_skills")),
  };

  importResult.textContent = "Analyzing and saving...";

  try {
    const result = await apiFetch("/imports/from-description", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    importResult.textContent = formatJson(result);
    importForm.reset();
    await refreshAll();
  } catch (error) {
    importResult.textContent = `Error: ${error.message}`;
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
    reportResult.innerHTML = `<p>Error: ${escapeHtml(error.message)}</p>`;
  }
});

function renderReport(result) {
  const recommendedResume = result.recommended_resume
    ? result.recommended_resume.name
    : "No recommendation";

  reportResult.innerHTML = `
    <div class="report-panel">
      <h3>${escapeHtml(result.company || "Unknown Company")} — ${escapeHtml(result.role || "Unknown Role")}</h3>
      <div class="metrics-grid">
        <div class="metric">
          <strong>${result.analysis.match_score}%</strong>
          <span>Match Score</span>
        </div>
        <div class="metric">
          <strong>${result.priority.priority_score}</strong>
          <span>Priority Score</span>
        </div>
        <div class="metric">
          <strong>${escapeHtml(result.priority.priority_level)}</strong>
          <span>Priority Level</span>
        </div>
        <div class="metric">
          <strong>${escapeHtml(recommendedResume)}</strong>
          <span>Recommended Resume</span>
        </div>
      </div>
    </div>

    <div class="report-panel">
      <h3>Job Analysis</h3>
      <p><strong>Job Family:</strong> ${escapeHtml(result.analysis.job_family)}</p>
      <p><strong>Role Level:</strong> ${escapeHtml(result.analysis.role_level)}</p>
      <p><strong>Location Type:</strong> ${escapeHtml(result.analysis.location_type)}</p>
      <p><strong>Detected Skills:</strong> ${escapeHtml(result.analysis.detected_skills.join(", ") || "None")}</p>
      <p><strong>Missing Skills:</strong> ${escapeHtml(result.analysis.missing_skills.join(", ") || "None")}</p>
    </div>

    <div class="report-panel">
      <h3>Action Items</h3>
      <ul>
        ${result.action_items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
      </ul>
    </div>

    <div class="report-panel">
      <h3>Suggested Notes</h3>
      <pre class="result-box">${escapeHtml(result.suggested_notes)}</pre>
    </div>
  `;
}

async function refreshAll() {
  await Promise.all([
    loadDashboard(),
    loadApplications(),
  ]);
}

refreshBtn.addEventListener("click", refreshAll);

refreshAll();
