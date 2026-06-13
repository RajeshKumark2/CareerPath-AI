from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InterviewQuestionViewSet, MockTestViewSet

router = DefaultRouter()
router.register(r'questions', InterviewQuestionViewSet, basename='question')
router.register(r'mock-tests', MockTestViewSet, basename='mock_test')

urlpatterns = [
    path('', include(router.urls)),
]

