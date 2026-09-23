from django.db import models


class Resume(models.Model):
    file = models.FileField(upload_to="resumes/")
    original_filename = models.CharField(max_length=255, blank=True)
    extracted_text = models.TextField(blank=True)
    skills = models.JSONField(default=list, blank=True)
    ats_score = models.FloatField(null=True, blank=True)
    ats_breakdown = models.JSONField(default=dict, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_filename or f"Resume #{self.pk}"


class JobDescription(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    required_skills = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} @ {self.company}"


class Match(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="matches")
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE, related_name="matches")
    match_score = models.FloatField()
    missing_skills = models.JSONField(default=list, blank=True)
    interview_questions = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-match_score"]

    def __str__(self):
        return f"{self.resume} <-> {self.job} ({self.match_score:.1f}%)"


class Application(models.Model):
    STATUS_CHOICES = [
        ("saved", "Saved"),
        ("applied", "Applied"),
        ("interview", "Interviewing"),
        ("offer", "Offer"),
        ("rejected", "Rejected"),
    ]

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="saved")
    notes = models.TextField(blank=True)
    applied_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.resume} -> {self.job} [{self.status}]"
