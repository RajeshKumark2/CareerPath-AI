from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResumeViewSet, ExperienceViewSet, EducationViewSet

router = DefaultRouter()
router.register(r'resumes', ResumeViewSet, basename='resume')
router.register(r'experiences', ExperienceViewSet, basename='experience')
router.register(r'educations', EducationViewSet, basename='education')

urlpatterns = [
    path('', include(router.urls)),
]
