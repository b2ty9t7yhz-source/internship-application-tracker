import re
from typing import Optional
from urllib.parse import urlparse, urlunparse

from sqlalchemy.orm import Session

from app.models import Application


CORPORATE_SUFFIXES = {
    "inc",
    "llc",
    "ltd",
    "corp",
    "corporation",
    "company",
    "co",
}

WORD_ALIASES = {
    "internship": "intern",
    "internships": "intern",
    "intern": "intern",
    "co-op": "intern",
    "coop": "intern",
    "graduate": "grad",
    "newgrad": "grad",
    "new": "new",
    "software": "software",
    "swe": "software",
    "developer": "engineer",
    "development": "engineer",
    "backend": "backend",
    "back": "backend",
    "back-end": "backend",
}


def normalize_word(word: str) -> str:
    return WORD_ALIASES.get(word, word)


def normalize_text(value: Optional[str]) -> str:
    if not value:
        return ""

    text = value.lower().strip()

    text = text.replace("back-end", "backend")
    text = text.replace("co-op", "coop")
    text = text.replace("new grad", "newgrad")

    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    words = []

    for word in text.split():
        if word in CORPORATE_SUFFIXES:
            continue

        words.append(normalize_word(word))

    return " ".join(words).strip()


def normalize_url(url: Optional[str]) -> str:
    if not url:
        return ""

    parsed = urlparse(url.strip())

    normalized = urlunparse(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path.rstrip("/"),
            "",
            "",
            "",
        )
    )

    return normalized


def calculate_similarity(a: str, b: str) -> int:
    a_words = set(normalize_text(a).split())
    b_words = set(normalize_text(b).split())

    if not a_words or not b_words:
        return 0

    overlap = a_words.intersection(b_words)
    union = a_words.union(b_words)

    return round(len(overlap) / len(union) * 100)


def check_duplicate_application(
    db: Session,
    company: str,
    role: str,
    link: Optional[str] = None,
) -> dict:
    normalized_link = normalize_url(link)

    applications = db.query(Application).all()

    best_match = None
    best_score = 0
    best_reason = "No duplicate found"

    for application in applications:
        existing_link = normalize_url(application.link)

        if normalized_link and existing_link and normalized_link == existing_link:
            return {
                "duplicate_found": True,
                "score": 100,
                "reason": "Same normalized link",
                "existing_application_id": application.id,
                "existing_company": application.company,
                "existing_role": application.role,
                "existing_link": application.link,
            }

        company_score = calculate_similarity(company, application.company)
        role_score = calculate_similarity(role, application.role)

        combined_score = round((company_score * 0.45) + (role_score * 0.55))

        if combined_score > best_score:
            best_score = combined_score
            best_match = application
            best_reason = (
                f"Company similarity: {company_score}%, "
                f"role similarity: {role_score}%"
            )

    if best_match and best_score >= 85:
        return {
            "duplicate_found": True,
            "score": best_score,
            "reason": best_reason,
            "existing_application_id": best_match.id,
            "existing_company": best_match.company,
            "existing_role": best_match.role,
            "existing_link": best_match.link,
        }

    return {
        "duplicate_found": False,
        "score": best_score,
        "reason": best_reason,
        "existing_application_id": best_match.id if best_match else None,
        "existing_company": best_match.company if best_match else None,
        "existing_role": best_match.role if best_match else None,
        "existing_link": best_match.link if best_match else None,
    }
