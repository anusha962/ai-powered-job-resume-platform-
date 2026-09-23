from rest_framework import serializers
from .models import Resume, JobDescription, Match, Application


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = [
            "id", "file", "original_filename", "extracted_text",
            "skills", "ats_score", "ats_breakdown", "uploaded_at",
        ]
        read_only_fields = [
            "extracted_text", "skills", "ats_score", "ats_breakdown", "uploaded_at",
        ]


class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = ["id", "title", "company", "description", "required_skills", "created_at"]
        read_only_fields = ["required_skills", "created_at"]


class MatchSerializer(serializers.ModelSerializer):
    job = JobDescriptionSerializer(read_only=True)

    class Meta:
        model = Match
        fields = [
            "id", "resume", "job", "match_score",
            "missing_skills", "interview_questions", "created_at",
        ]
        read_only_fields = fields


class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    company = serializers.CharField(source="job.company", read_only=True)

    class Meta:
        model = Application
        fields = [
            "id", "resume", "job", "job_title", "company", "status",
            "notes", "applied_date", "updated_at", "created_at",
        ]
