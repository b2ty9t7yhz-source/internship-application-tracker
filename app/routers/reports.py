from fastapi import APIRouter

from app import schemas
from app.services.intelligence_report import generate_application_intelligence_report

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)


@router.post(
    "/application-intelligence",
    response_model=schemas.ApplicationIntelligenceReportResponse,
)
def create_application_intelligence_report(
    payload: schemas.ApplicationIntelligenceReportRequest,
):
    resume_versions = [
        resume.model_dump()
        for resume in payload.resume_versions
    ]

    report = generate_application_intelligence_report(
        description=payload.description,
        user_skills=payload.user_skills,
        deadline=payload.deadline,
        preferred_locations=payload.preferred_locations,
        resume_versions=resume_versions,
    )

    return {
        "company": payload.company,
        "role": payload.role,
        **report,
    }
