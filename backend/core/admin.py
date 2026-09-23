from django.contrib import admin
from .models import Resume, JobDescription, Match, Application

admin.site.register(Resume)
admin.site.register(JobDescription)
admin.site.register(Match)
admin.site.register(Application)
