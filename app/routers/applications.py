from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.services.duplicate_detector import check_duplicate_application
from app.database import get_db

router = APIRouter(
    prefix="/applications",
    tags=["applications"],
)

@router.post("/", response_model=schemas.ApplicationRead, status_code=201)
def create_application(
    application: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
):
    return crud.create_application(db=db, application=application)

@router.get("/", response_model=List[schemas.ApplicationRead])
def read_applications(
    company: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_applications(
        db=db,
        company=company,
        status=status,
        skip=skip,
        limit=limit,
    )

@router.get("/{application_id}", response_model=schemas.ApplicationRead)
def read_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    db_application = crud.get_application(db=db, application_id=application_id)

    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return db_application

@router.put("/{application_id}", response_model=schemas.ApplicationRead)
def update_application(
    application_id: int,
    updates: schemas.ApplicationUpdate,
    db: Session = Depends(get_db),
):
    db_application = crud.get_application(db=db, application_id=application_id)

    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return crud.update_application(
        db=db,
        db_application=db_application,
        updates=updates,
    )

@router.delete("/{application_id}", response_model=schemas.ApplicationRead)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    db_application = crud.get_application(db=db, application_id=application_id)

    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return crud.delete_application(db=db, db_application=db_application)


@router.post(
    "/check-duplicate",
    response_model=schemas.DuplicateCheckResponse,
)
def check_duplicate(
    payload: schemas.DuplicateCheckRequest,
    db: Session = Depends(get_db),
):
    return check_duplicate_application(
        db=db,
        company=payload.company,
        role=payload.role,
        link=payload.link,
    )

