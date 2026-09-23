from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Resume, JobDescription, Match, Application
from .serializers import (
    ResumeSerializer, JobDescriptionSerializer, MatchSerializer, ApplicationSerializer,
)
from .utils.pdf_extract import extract_text
from .utils.skill_extraction import extract_skills
from .utils.ats_scoring import score_resume
from .utils.rag_matcher import rank_jobs_for_resume, build_match


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def create(self, request, *args, **kwargs):
        """Upload a resume: extract text, extract skills, compute ATS score."""
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        resume = Resume.objects.create(file=file_obj, original_filename=file_obj.name)

        text = extract_text(resume.file, file_obj.name)
        skills = extract_skills(text)
        scoring = score_resume(text, skills)

        resume.extracted_text = text
        resume.skills = skills
        resume.ats_score = scoring["score"]
        resume.ats_breakdown = scoring["breakdown"]
        resume.save()

        return Response(ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def recommendations(self, request, pk=None):
        """Retrieval step of the RAG pipeline: rank all jobs against this resume."""
        resume = self.get_object()
        jobs = list(JobDescription.objects.all())
        ranked = rank_jobs_for_resume(resume.extracted_text, jobs)
        data = [
            {
                "job": JobDescriptionSerializer(r["job"]).data,
                "similarity_pct": r["similarity_pct"],
            }
            for r in ranked[:10]
        ]
        return Response(data)

    @action(detail=True, methods=["post"], url_path="match")
    def match_with_job(self, request, pk=None):
        """Generation step: build (or refresh) a full Match against a given job id."""
        resume = self.get_object()
        job_id = request.data.get("job_id")
        if not job_id:
            return Response({"error": "job_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            job = JobDescription.objects.get(pk=job_id)
        except JobDescription.DoesNotExist:
            return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

        result = build_match(resume, job, resume.skills)
        match, _ = Match.objects.update_or_create(
            resume=resume, job=job,
            defaults={
                "match_score": result["match_score"],
                "missing_skills": result["missing_skills"],
                "interview_questions": result["interview_questions"],
            },
        )
        return Response(MatchSerializer(match).data, status=status.HTTP_200_OK)


class JobDescriptionViewSet(viewsets.ModelViewSet):
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer

    def perform_create(self, serializer):
        job = serializer.save()
        job.required_skills = extract_skills(job.description)
        job.save()


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        resume_id = self.request.query_params.get("resume")
        if resume_id:
            qs = qs.filter(resume_id=resume_id)
        return qs


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        resume_id = self.request.query_params.get("resume")
        if resume_id:
            qs = qs.filter(resume_id=resume_id)
        return qs
