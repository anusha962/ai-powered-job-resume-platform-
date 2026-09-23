"""Thin wrapper around the Anthropic API for the generative parts of the
RAG pipeline (tailored interview questions, resume-gap summaries).

If ANTHROPIC_API_KEY isn't set, falls back to simple templated output so
the rest of the app still works without an API key configured.
"""
import json
import os
from django.conf import settings


def _client():
    import anthropic

    api_key = settings.ANTHROPIC_API_KEY or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    return anthropic.Anthropic(api_key=api_key)


def generate_interview_questions(resume_text: str, job_description: str, missing_skills: list[str]) -> list[str]:
    """Generate 5 tailored interview questions grounded in the resume and
    job description (the retrieved context from the RAG pipeline)."""
    client = _client()
    if client is None:
        return _fallback_questions(missing_skills)

    prompt = f"""You are an expert technical interviewer. Based on the candidate's
resume and the target job description below, write 5 tailored interview
questions. Mix behavioral questions grounded in the resume's actual
experience with technical questions probing the candidate's gaps.

Candidate resume (excerpt):
{resume_text[:3000]}

Job description:
{job_description[:2000]}

Skills the candidate is missing relative to this job: {", ".join(missing_skills) or "none identified"}

Respond ONLY with a JSON array of 5 strings (the questions), no other text."""

    try:
        response = client.messages.create(
            model=settings.LLM_MODEL,
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(block.text for block in response.content if block.type == "text")
        text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        questions = json.loads(text)
        if isinstance(questions, list) and questions:
            return questions[:5]
    except Exception:
        pass
    return _fallback_questions(missing_skills)


def _fallback_questions(missing_skills: list[str]) -> list[str]:
    questions = [
        "Walk me through a project on your resume you're most proud of — what was your specific role?",
        "Tell me about a time you had to learn a new technology quickly to complete a task.",
        "Describe a challenging bug or production issue you resolved. What was your process?",
    ]
    for skill in missing_skills[:2]:
        questions.append(f"How would you approach getting up to speed with {skill} for this role?")
    return questions[:5]
