from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.services.job_analyzer import analyze_job_description
from app.services.duplicate_detector import check_duplicate_application
from app.services.greenhouse_importer import import_greenhouse_jobs_preview

router = APIRouter(
    prefix="/imports",
    tags=["imports"],
)


@router.post(
    "/from-description",
    response_model=schemas.ImportedApplicationResponse,
    status_code=201,
)
def import_application_from_description(
    payload: schemas.ImportFromDescriptionRequest,
    db: Session = Depends(get_db),
):
    analysis = analyze_job_description(
        description=payload.description,
        user_skills=payload.user_skills,
    )

    analysis_notes = (
        f"Job Analysis Summary\n"
        f"- Match score: {analysis['match_score']}%\n"
        f"- Role level: {analysis['role_level']}\n"
        f"- Job family: {analysis['job_family']}\n"
        f"- Location type: {analysis['location_type']}\n"
        f"- Matched skills: {', '.join(analysis['matched_skills']) or 'None'}\n"
        f"- Missing skills: {', '.join(analysis['missing_skills']) or 'None'}\n"
        f"- Recommendation: {analysis['recommendation']}\n"
    )

    if payload.notes:
        combined_notes = f"{payload.notes}\n\n{analysis_notes}"
    else:
        combined_notes = analysis_notes

    application_data = schemas.ApplicationCreate(
        company=payload.company,
        role=payload.role,
        link=payload.link,
        type=payload.type or analysis["job_family"],
        location=payload.location or analysis["location_type"],
        source=payload.source,
        status=payload.status,
        deadline=payload.deadline,
        date_applied=payload.date_applied,
        resume_version=payload.resume_version,
        notes=combined_notes,
    )

    duplicate_check = check_duplicate_application(
        db=db,
        company=application_data.company,
        role=application_data.role,
        link=application_data.link,
    )

    if duplicate_check["duplicate_found"]:
        existing_application = crud.get_application(
            db=db,
            application_id=duplicate_check["existing_application_id"],
        )

        return {
            "application": existing_application,
            "analysis": analysis,
        }

    application = crud.create_application(
        db=db,
        application=application_data,
    )

    return {
        "application": application,
        "analysis": analysis,
    }


@router.post(
    "/greenhouse",
    response_model=schemas.GreenhouseImportResponse,
)
def import_greenhouse_jobs(
    payload: schemas.GreenhouseImportRequest,
    db: Session = Depends(get_db),
):
    results = import_greenhouse_jobs_preview(
        board_token=payload.board_token,
        company=payload.company,
        keywords=payload.keywords,
        locations=payload.locations,
        user_skills=payload.user_skills,
        limit=payload.limit,
    )

    saved_jobs = 0

    if payload.save_results:
        for item in results:
            job = item["job"]
            analysis = item["analysis"]

            analysis_notes = (
                f"Imported from Greenhouse\n"
                f"- Match score: {analysis['match_score']}%\n"
                f"- Role level: {analysis['role_level']}\n"
                f"- Job family: {analysis['job_family']}\n"
                f"- Location type: {analysis['location_type']}\n"
                f"- Matched skills: {', '.join(analysis['matched_skills']) or 'None'}\n"
                f"- Missing skills: {', '.join(analysis['missing_skills']) or 'None'}\n"
                f"- Recommendation: {analysis['recommendation']}\n"
            )

            application_data = schemas.ApplicationCreate(
                company=job["company"],
                role=job["role"],
                link=job["link"],
                type=analysis["job_family"],
                location=job["location"] or analysis["location_type"],
                source=job["source"],
                status="Saved",
                notes=analysis_notes,
            )

            crud.create_application(
                db=db,
                application=application_data,
            )

            saved_jobs += 1

    return {
        "board_token": payload.board_token,
        "company": payload.company,
        "matched_jobs": len(results),
        "saved_jobs": saved_jobs,
        "results": results,
    }

