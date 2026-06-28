from datetime import date
from typing import List, Optional

from app.services.job_analyzer import analyze_job_description
from app.services.priority_scorer import score_job_priority
from app.services.resume_recommender import recommend_resume_version


def build_action_items(
    priority_level: str,
    missing_skills: List[str],
    recommended_resume_name: Optional[str],
    deadline: Optional[date],
) -> List[str]:
    action_items = []

    if priority_level == "High":
        action_items.append("Apply soon because this role appears to be a strong fit.")
    elif priority_level == "Medium":
        action_items.append("Apply after a quick resume review.")
    elif priority_level == "Low":
        action_items.append("Save this role as a backup and improve fit before applying.")
    else:
        action_items.append("Do not prioritize this role unless there is a strong personal reason.")

    if recommended_resume_name:
        action_items.append(f"Use resume version: {recommended_resume_name}.")

    if missing_skills:
        top_missing = ", ".join(missing_skills[:3])
        action_items.append(f"Review or learn missing skills: {top_missing}.")

    if deadline:
        action_items.append(f"Check the deadline and apply before {deadline.isoformat()}.")

    return action_items


def build_suggested_notes(
    analysis: dict,
    priority: dict,
    recommended_resume_name: Optional[str],
) -> str:
    return (
        "Application Intelligence Summary\n"
        f"- Match score: {analysis['match_score']}%\n"
        f"- Priority score: {priority['priority_score']}\n"
        f"- Priority level: {priority['priority_level']}\n"
        f"- Job family: {analysis['job_family']}\n"
        f"- Role level: {analysis['role_level']}\n"
        f"- Location type: {analysis['location_type']}\n"
        f"- Detected skills: {', '.join(analysis['detected_skills']) or 'None'}\n"
        f"- Matched skills: {', '.join(analysis['matched_skills']) or 'None'}\n"
        f"- Missing skills: {', '.join(analysis['missing_skills']) or 'None'}\n"
        f"- Recommended resume: {recommended_resume_name or 'No resume recommendation'}\n"
        f"- Recommendation: {priority['recommendation']}\n"
    )


def generate_application_intelligence_report(
    description: str,
    user_skills: List[str],
    deadline: Optional[date] = None,
    preferred_locations: Optional[List[str]] = None,
    resume_versions: Optional[List[dict]] = None,
) -> dict:
    preferred_locations = preferred_locations or []
    resume_versions = resume_versions or []

    analysis = analyze_job_description(
        description=description,
        user_skills=user_skills,
    )

    priority = score_job_priority(
        match_score=analysis["match_score"],
        role_level=analysis["role_level"],
        location_type=analysis["location_type"],
        deadline=deadline,
        preferred_locations=preferred_locations,
        missing_skills=analysis["missing_skills"],
    )

    resume_recommendation = None
    recommended_resume = None
    recommended_resume_name = None

    if resume_versions:
        resume_recommendation = recommend_resume_version(
            description=description,
            resume_versions=resume_versions,
        )
        recommended_resume = resume_recommendation["recommended_resume"]

        if recommended_resume:
            recommended_resume_name = recommended_resume["name"]

    action_items = build_action_items(
        priority_level=priority["priority_level"],
        missing_skills=analysis["missing_skills"],
        recommended_resume_name=recommended_resume_name,
        deadline=deadline,
    )

    suggested_notes = build_suggested_notes(
        analysis=analysis,
        priority=priority,
        recommended_resume_name=recommended_resume_name,
    )

    return {
        "analysis": analysis,
        "priority": priority,
        "recommended_resume": recommended_resume,
        "all_resume_scores": resume_recommendation["all_resume_scores"] if resume_recommendation else [],
        "action_items": action_items,
        "suggested_notes": suggested_notes,
    }
