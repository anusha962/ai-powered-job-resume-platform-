"""Lightweight RAG (retrieval-augmented generation) pipeline.

Retrieval: TF-IDF + cosine similarity ranks job descriptions against a
resume's text — no external vector DB needed, so it deploys cleanly on
Render's free tier.

Augmented generation: the top-matching job description (the "retrieved
context") plus the resume's missing skills are fed to the LLM to generate
tailored interview questions — grounding the generation in real, retrieved
job-description content rather than the model's own assumptions.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .skill_extraction import compare_skills
from . import llm_client


def rank_jobs_for_resume(resume_text: str, jobs: list) -> list[dict]:
    """Retrieve & rank JobDescription objects by textual similarity to a resume.

    Returns a list of {"job": job, "similarity_pct": float} sorted descending.
    """
    if not jobs:
        return []

    corpus = [resume_text] + [j.description for j in jobs]
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    tfidf = vectorizer.fit_transform(corpus)
    resume_vec, job_vecs = tfidf[0:1], tfidf[1:]
    sims = cosine_similarity(resume_vec, job_vecs)[0]

    ranked = sorted(
        (
            {"job": job, "similarity_pct": round(float(sim) * 100, 1)}
            for job, sim in zip(jobs, sims)
        ),
        key=lambda r: r["similarity_pct"],
        reverse=True,
    )
    return ranked


def build_match(resume, job, resume_skills: list[str]) -> dict:
    """Build a full match result between one resume and one job:
    skill comparison (retrieval-grounded) + LLM-generated interview questions.
    """
    skill_comparison = compare_skills(resume_skills, job.required_skills)

    questions = llm_client.generate_interview_questions(
        resume_text=resume.extracted_text,
        job_description=job.description,
        missing_skills=skill_comparison["missing_skills"],
    )

    # Blend skill coverage with any additional heuristic weighting here.
    match_score = skill_comparison["coverage_pct"]

    return {
        "match_score": match_score,
        "missing_skills": skill_comparison["missing_skills"],
        "matched_skills": skill_comparison["matched_skills"],
        "interview_questions": questions,
    }
