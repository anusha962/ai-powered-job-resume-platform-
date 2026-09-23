"""Heuristic ATS-style resume scoring.

Combines simple structural checks (things real ATS parsers care about)
with skill-density signals. Returns a 0-100 score plus a breakdown so the
frontend can show *why* a resume scored the way it did.
"""
import re

SECTION_KEYWORDS = {
    "contact": [r"email", r"phone", r"linkedin", r"@\w+\.\w+"],
    "experience": [r"experience", r"work history", r"employment"],
    "education": [r"education", r"university", r"degree", r"b\.?tech|b\.?sc|m\.?tech|m\.?sc"],
    "skills": [r"skills", r"technologies", r"tech stack"],
    "projects": [r"projects?"],
}

# Rough word-count band for a well-formatted single/double page resume
IDEAL_WORD_RANGE = (300, 900)


def _has_section(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def score_resume(text: str, extracted_skills: list[str]) -> dict:
    """Return {"score": float, "breakdown": {...}} for a resume."""
    breakdown = {}

    # 1) Structural sections present (40 points)
    section_hits = {name: _has_section(text, pats) for name, pats in SECTION_KEYWORDS.items()}
    sections_found = sum(section_hits.values())
    section_score = round((sections_found / len(SECTION_KEYWORDS)) * 40, 1)
    breakdown["sections"] = {"found": section_hits, "points": section_score, "max": 40}

    # 2) Skill density / breadth (35 points) — capped so listing 100 buzzwords
    #    doesn't game the score; rewards a healthy, realistic skill set.
    skill_count = len(extracted_skills)
    skill_score = round(min(skill_count / 12, 1.0) * 35, 1)
    breakdown["skills"] = {"count": skill_count, "points": skill_score, "max": 35}

    # 3) Length / conciseness (15 points)
    word_count = len(text.split())
    low, high = IDEAL_WORD_RANGE
    if low <= word_count <= high:
        length_score = 15.0
    else:
        distance = min(abs(word_count - low), abs(word_count - high))
        length_score = max(0.0, 15 - (distance / 50))
    breakdown["length"] = {"word_count": word_count, "points": round(length_score, 1), "max": 15}

    # 4) Quantified achievements — numbers/percentages signal impact (10 points)
    numbers_found = len(re.findall(r"\b\d+%|\b\d+\+|\$\d+|\b\d{2,}\b", text))
    quant_score = round(min(numbers_found / 6, 1.0) * 10, 1)
    breakdown["quantified_impact"] = {"signals_found": numbers_found, "points": quant_score, "max": 10}

    total = round(section_score + skill_score + length_score + quant_score, 1)
    total = max(0.0, min(100.0, total))

    return {"score": total, "breakdown": breakdown}
