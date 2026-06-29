# Internship Application Intelligence Tracker

A FastAPI-based backend and web app for tracking internship applications, analyzing job descriptions, recommending resume versions, and prioritizing roles.

## Overview

Students applying to internships often lose track of:

- Which companies they saved or applied to
- Which resume version they used
- Which roles are high priority
- Which skills are missing from a job description
- Which applications need follow-up

This project solves that problem with an application tracker plus job intelligence features.

## Features

### Application Tracking

- Add applications
- View all applications
- View one application
- Update application status
- Delete applications
- Track company, role, link, source, status, deadline, location, notes, and resume version

### Job Intelligence

- Analyze job descriptions
- Detect skills such as Python, SQL, REST API, FastAPI, Docker, AWS, Git, and more
- Identify job family such as Backend, Data, Web / Full Stack, AI / ML, QA, or IT
- Detect role level such as Internship, Entry Level, or Senior
- Calculate match score based on user skills
- Identify matched and missing skills

### Import Workflow

- Paste a job description
- Analyze the role automatically
- Generate notes
- Save the role as an application

### Resume Recommendation

- Compare job descriptions against multiple resume versions
- Recommend the best resume version for a role
- Explain matched and missing skills

### Priority Scoring

- Score roles based on match score, role level, location type, deadline, and missing skills
- Return priority level and action items

### Dashboard

- View total applications
- View saved and applied counts
- View interview count
- View upcoming deadlines

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- pytest
- HTML
- CSS
- JavaScript
- GitHub Actions

## Project Structure

    internship-application-tracker/
      app/
        main.py
        database.py
        models.py
        schemas.py
        crud.py
        routers/
        services/
        static/
      tests/
      docs/
      requirements.txt
      README.md

## How to Run Locally

Create and activate a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Start the app:

    python -m uvicorn app.main:app --reload

Open the web UI:

    http://127.0.0.1:8000/ui

Open the API docs:

    http://127.0.0.1:8000/docs

## Running Tests

    python -m pytest -q

## Main API Endpoints

### Applications

    POST   /applications/
    GET    /applications/
    GET    /applications/{application_id}
    PUT    /applications/{application_id}
    DELETE /applications/{application_id}
    POST   /applications/check-duplicate

### Job Analysis

    POST /jobs/analyze-description
    POST /jobs/score-priority

### Imports

    POST /imports/from-description
    POST /imports/greenhouse

### Stats

    GET /stats/summary
    GET /stats/applications-by-status
    GET /stats/applications-by-source
    GET /stats/upcoming-deadlines

### Resume Recommendation

    POST /resumes/recommend

### Reports

    POST /reports/application-intelligence

## Demo Flow

See:

    docs/demo_script.md

## Current Status

The project currently supports application tracking, job description analysis, import workflow, resume recommendation, priority scoring, dashboard statistics, and a basic web frontend.

## Future Improvements

- User authentication
- PostgreSQL deployment database
- Docker setup
- Better frontend UI
- Saved search profiles
- Email reminders
- Calendar reminders
- AI-powered job description summarization
- Deployment to a public URL

## Docker

Build the Docker image:

    docker build -t internship-application-tracker .

Run the app with Docker:

    docker run -p 8000:8000 internship-application-tracker

Or use Docker Compose:

    docker compose up --build

Then open:

    http://127.0.0.1:8000/ui

Health check:

    http://127.0.0.1:8000/health

## Makefile Commands

Run locally:

    make run

Run tests:

    make test

Build Docker image:

    make docker-build

Run Docker container:

    make docker-run

## Database Migrations

This project includes Alembic migrations.

Run migrations:

    alembic upgrade head

Check migration history:

    alembic history

Migration docs:

    docs/database_migrations.md

## Deployment

This project is prepared for Render deployment.

Recommended Render settings:

    Build Command: pip install -r requirements.txt
    Start Command: alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT

After deployment:

    /ui      Web frontend
    /docs    API documentation
    /health  Health check

See:

    docs/deployment.md

## Live Demo

The project is deployed on Render.

Web UI:

    https://internship-application-tracker-l6ha.onrender.com/ui

API Docs:

    https://internship-application-tracker-l6ha.onrender.com/docs

Health Check:

    https://internship-application-tracker-l6ha.onrender.com/health

Note: The app is hosted on a free Render instance, so the first request may take extra time if the service has been inactive.
