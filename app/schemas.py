from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict

ApplicationStatus = Literal[
    "Saved",
    "Applied",
    "OA",
    "Interview",
    "Rejected",
    "Offer",
    "No Response",
]

class ApplicationBase(BaseModel):
    company: str
    role: str
    link: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    source: Optional[str] = None
    status: ApplicationStatus = "Saved"
    deadline: Optional[date] = None
    date_applied: Optional[date] = None
    resume_version: Optional[str] = None
    notes: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    link: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    source: Optional[str] = None
    status: Optional[ApplicationStatus] = None
    deadline: Optional[date] = None
    date_applied: Optional[date] = None
    resume_version: Optional[str] = None
    notes: Optional[str] = None

class ApplicationRead(ApplicationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JobDescriptionAnalysisRequest(BaseModel):
    description: str
    user_skills: list[str] = []


class JobDescriptionAnalysisResponse(BaseModel):
    detected_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    match_score: int
    role_level: str
    job_family: str
    location_type: str
    recommendation: str


class ImportFromDescriptionRequest(BaseModel):
    company: str
    role: str
    description: str
    link: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    source: Optional[str] = "Manual Import"
    status: ApplicationStatus = "Saved"
    deadline: Optional[date] = None
    date_applied: Optional[date] = None
    resume_version: Optional[str] = None
    notes: Optional[str] = None
    user_skills: list[str] = []


class ImportedApplicationResponse(BaseModel):
    application: ApplicationRead
    analysis: JobDescriptionAnalysisResponse


class GreenhouseImportRequest(BaseModel):
    board_token: str
    company: str
    keywords: list[str] = []
    locations: list[str] = []
    user_skills: list[str] = []
    limit: int = 10
    save_results: bool = False


class GreenhouseJobPreview(BaseModel):
    company: str
    role: str
    link: Optional[str] = None
    location: Optional[str] = None
    source: str
    description: str
    greenhouse_job_id: Optional[int] = None


class GreenhouseImportItem(BaseModel):
    job: GreenhouseJobPreview
    analysis: JobDescriptionAnalysisResponse


class GreenhouseImportResponse(BaseModel):
    board_token: str
    company: str
    matched_jobs: int
    saved_jobs: int
    results: list[GreenhouseImportItem]


class GreenhouseImportRequest(BaseModel):
    board_token: str
    company: str
    keywords: list[str] = []
    locations: list[str] = []
    user_skills: list[str] = []
    limit: int = 10
    save_results: bool = False


class GreenhouseJobPreview(BaseModel):
    company: str
    role: str
    link: Optional[str] = None
    location: Optional[str] = None
    source: str
    description: str
    greenhouse_job_id: Optional[int] = None


class GreenhouseImportItem(BaseModel):
    job: GreenhouseJobPreview
    analysis: JobDescriptionAnalysisResponse


class GreenhouseImportResponse(BaseModel):
    board_token: str
    company: str
    matched_jobs: int
    saved_jobs: int
    results: list[GreenhouseImportItem]


class DuplicateCheckRequest(BaseModel):
    company: str
    role: str
    link: Optional[str] = None


class DuplicateCheckResponse(BaseModel):
    duplicate_found: bool
    score: int
    reason: str
    existing_application_id: Optional[int] = None
    existing_company: Optional[str] = None
    existing_role: Optional[str] = None
    existing_link: Optional[str] = None


class JobPriorityScoreRequest(BaseModel):
    description: str
    user_skills: list[str] = []
    deadline: Optional[date] = None
    preferred_locations: list[str] = []


class JobPriorityScoreResponse(BaseModel):
    priority_score: int
    priority_level: str
    recommendation: str
    reasons: list[str]
    analysis: JobDescriptionAnalysisResponse


class ResumeVersionInput(BaseModel):
    name: str
    focus_area: str
    skills: list[str]
    notes: Optional[str] = None


class ResumeRecommendationRequest(BaseModel):
    description: str
    resume_versions: list[ResumeVersionInput]


class ResumeScore(BaseModel):
    name: str
    focus_area: str
    score: int
    matched_skills: list[str]
    missing_skills: list[str]
    reasons: list[str]


class ResumeRecommendationResponse(BaseModel):
    recommended_resume: Optional[ResumeScore] = None
    all_resume_scores: list[ResumeScore]
    job_analysis: JobDescriptionAnalysisResponse


class ApplicationIntelligenceReportRequest(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    description: str
    user_skills: list[str] = []
    deadline: Optional[date] = None
    preferred_locations: list[str] = []
    resume_versions: list[ResumeVersionInput] = []


class PrioritySummary(BaseModel):
    priority_score: int
    priority_level: str
    recommendation: str
    reasons: list[str]


class ApplicationIntelligenceReportResponse(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    analysis: JobDescriptionAnalysisResponse
    priority: PrioritySummary
    recommended_resume: Optional[ResumeScore] = None
    all_resume_scores: list[ResumeScore]
    action_items: list[str]
    suggested_notes: str
