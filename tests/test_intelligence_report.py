from datetime import date, timedelta

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_application_intelligence_report_endpoint():
    response = client.post(
        "/reports/application-intelligence",
        json={
            "company": "Demo Company",
            "role": "Backend Engineer Intern",
            "description": "We are hiring a remote backend Software Engineer Intern with Python, SQL, REST API, FastAPI, Docker, and AWS experience.",
            "user_skills": ["Python", "SQL", "REST API", "FastAPI", "Git"],
            "deadline": (date.today() + timedelta(days=7)).isoformat(),
            "preferred_locations": ["Remote"],
            "resume_versions": [
                {
                    "name": "resume_general_swe_v1",
                    "focus_area": "General SWE",
                    "skills": ["Python", "Java", "Git", "Data Structures"],
                },
                {
                    "name": "resume_backend_v1",
                    "focus_area": "Backend",
                    "skills": ["Python", "SQL", "REST API", "FastAPI", "Git", "Docker"],
                },
                {
                    "name": "resume_data_v1",
                    "focus_area": "Data",
                    "skills": ["Python", "SQL", "Pandas", "Machine Learning"],
                },
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["company"] == "Demo Company"
    assert data["role"] == "Backend Engineer Intern"
    assert data["analysis"]["role_level"] == "Internship"
    assert data["analysis"]["job_family"] == "Backend"
    assert data["priority"]["priority_score"] > 0
    assert data["recommended_resume"]["name"] == "resume_backend_v1"
    assert len(data["action_items"]) > 0
    assert "Application Intelligence Summary" in data["suggested_notes"]
