# Project Showcase: Internship Application Intelligence Tracker

## One-Sentence Summary

A FastAPI-based web application that helps students track internship applications, analyze job descriptions, recommend resume versions, and prioritize roles.

## Live Demo

Web UI:

    https://internship-application-tracker-l6ha.onrender.com/ui

API Docs:

    https://internship-application-tracker-l6ha.onrender.com/docs

Health Check:

    https://internship-application-tracker-l6ha.onrender.com/health

## Problem

Students applying to internships often manage applications manually with spreadsheets. This becomes difficult when tracking multiple companies, deadlines, statuses, resume versions, job descriptions, and follow-up actions.

## Solution

This project provides an application tracker with job intelligence features. Users can save applications, analyze job descriptions, detect matched and missing skills, calculate priority scores, recommend resume versions, and generate action items.

## Core Features

- Application CRUD: create, read, update, and delete internship applications
- Dashboard with application statistics
- Job description analyzer
- Skill matching and missing skill detection
- Resume version recommender
- Application priority scoring
- Job description import workflow
- Duplicate job detector
- Intelligence report generator
- Web frontend
- FastAPI Swagger API documentation
- Docker support
- GitHub Actions test workflow
- Render deployment

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- pytest
- Alembic
- Docker
- HTML
- CSS
- JavaScript
- GitHub Actions
- Render

## Engineering Highlights

- Designed a modular FastAPI backend with routers, services, schemas, models, and CRUD layers.
- Implemented SQLAlchemy models and SQLite persistence for application tracking.
- Built REST API endpoints for application tracking, job analysis, imports, stats, resume recommendations, and intelligence reports.
- Added pytest tests for backend services and API endpoints.
- Added GitHub Actions CI to run tests automatically on push and pull requests.
- Added Dockerfile and docker-compose configuration for containerized deployment.
- Deployed the application publicly using Render.
- Built a lightweight frontend that interacts with the FastAPI backend.

## Demo Flow

1. Open the web UI.
2. Add an internship application manually.
3. Paste a job description into the analyzer.
4. Show detected skills, matched skills, missing skills, and match score.
5. Import a job description as an application.
6. Generate an application intelligence report.
7. Show API docs and test endpoints through Swagger.

## Future Improvements

- Add user authentication
- Add PostgreSQL database for production
- Add persistent storage on deployment
- Add saved search profiles
- Add email reminders
- Add calendar reminders
- Improve frontend design
- Add AI-powered job description summarization
