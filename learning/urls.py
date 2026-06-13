from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LearningRoadmapViewSet, UserLearningProgressViewSet

router = DefaultRouter()
router.register(r'roadmaps', LearningRoadmapViewSet, basename='roadmap')
router.register(r'progress', UserLearningProgressViewSet, basename='progress')

urlpatterns = [
    path('', include(router.urls)),
]
