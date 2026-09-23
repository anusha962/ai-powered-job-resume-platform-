from rest_framework.routers import DefaultRouter
from .views import ResumeViewSet, JobDescriptionViewSet, MatchViewSet, ApplicationViewSet

router = DefaultRouter()
router.register(r"resumes", ResumeViewSet, basename="resume")
router.register(r"jobs", JobDescriptionViewSet, basename="job")
router.register(r"matches", MatchViewSet, basename="match")
router.register(r"applications", ApplicationViewSet, basename="application")

urlpatterns = router.urls
