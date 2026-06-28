from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_duplicate_detector_same_link():
    create_response = client.post(
        "/applications/",
        json={
            "company": "Duplicate Demo Company",
            "role": "Software Engineer Intern",
            "link": "https://example.com/jobs/duplicate-demo?utm_source=linkedin",
            "type": "SWE Intern",
            "location": "Remote",
            "source": "LinkedIn",
            "status": "Saved",
            "resume_version": "resume_v0",
            "notes": "Created for duplicate detector test.",
        },
    )

    assert create_response.status_code == 201

    check_response = client.post(
        "/applications/check-duplicate",
        json={
            "company": "Duplicate Demo Company",
            "role": "Software Engineer Intern",
            "link": "https://example.com/jobs/duplicate-demo",
        },
    )

    assert check_response.status_code == 200

    data = check_response.json()

    assert data["duplicate_found"] is True
    assert data["score"] == 100
    assert data["existing_application_id"] is not None


def test_duplicate_detector_company_and_role_similarity():
    create_response = client.post(
        "/applications/",
        json={
            "company": "Similarity Demo Inc.",
            "role": "Backend Engineer Intern",
            "link": "https://example.com/jobs/similarity-demo-a",
            "type": "Backend",
            "location": "Remote",
            "source": "Company Website",
            "status": "Saved",
        },
    )

    assert create_response.status_code == 201

    check_response = client.post(
        "/applications/check-duplicate",
        json={
            "company": "Similarity Demo",
            "role": "Backend Engineer Internship",
            "link": "https://another-site.com/jobs/similarity-demo-b",
        },
    )

    assert check_response.status_code == 200

    data = check_response.json()

    assert data["duplicate_found"] is True
    assert data["score"] >= 85
