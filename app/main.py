from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import applications, job_analysis, imports, stats, resumes, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Internship Application Intelligence Tracker",
    description="A backend API for tracking internship applications, deadlines, resume versions, follow-ups, and application statistics.",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(applications.router)
app.include_router(job_analysis.router)
app.include_router(imports.router)
app.include_router(stats.router)
app.include_router(resumes.router)
app.include_router(reports.router)

@app.get("/")
def read_root():
    return {
        "message": "Internship Application Intelligence Tracker API",
        "status": "V1 CRUD in progress"
    }


@app.get("/ui")
def read_ui():
    return FileResponse("app/static/index.html")
