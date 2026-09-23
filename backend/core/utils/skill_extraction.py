"""NLP-based skill extraction.

Uses lightweight keyword/phrase matching over a curated skill taxonomy
(fast, no heavy model download -> deploys fine on Render's free tier).
If ANTHROPIC_API_KEY is configured, results can optionally be refined by
the LLM (see llm_client.refine_skills) for messier/creative resume formats.
"""
import re
from .skill_taxonomy import SKILL_TAXONOMY

# Sort longest-first so multi-word skills ("django rest framework") are
# matched before their substrings ("django").
_SORTED_SKILLS = sorted(SKILL_TAXONOMY, key=len, reverse=True)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def extract_skills(text: str) -> list[str]:
    """Return the list of taxonomy skills found in the given text."""
    normalized = _normalize(text)
    found = []
    for skill in _SORTED_SKILLS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
        if re.search(pattern, normalized):
            found.append(skill)
    # De-duplicate while preserving order, title-case for display
    seen = set()
    result = []
    for s in found:
        if s not in seen:
            seen.add(s)
            result.append(s)
    return result


def compare_skills(resume_skills: list[str], job_skills: list[str]) -> dict:
    """Compare resume skills against a job's required skills."""
    resume_set = {s.lower() for s in resume_skills}
    job_set = {s.lower() for s in job_skills}
    matched = sorted(resume_set & job_set)
    missing = sorted(job_set - resume_set)
    extra = sorted(resume_set - job_set)
    coverage = (len(matched) / len(job_set) * 100) if job_set else 100.0
    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "coverage_pct": round(coverage, 1),
    }
