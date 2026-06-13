from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Resume, Experience, Education, ResumeSkill, Certification
from .serializers import ResumeSerializer, ExperienceSerializer, EducationSerializer, CertificationSerializer
from django.http import FileResponse
import os

class ResumeViewSet(viewsets.ModelViewSet):
    """
    Resume management
    """
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_resume(self, request):
        """
        Get user's resume
        """
        try:
            resume = Resume.objects.get(user=request.user)
            serializer = ResumeSerializer(resume)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Resume.DoesNotExist:
            return Response({'error': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create_resume(self, request):
        """
        Create a new resume
        """
        try:
            resume = Resume.objects.get(user=request.user)
            return Response({'error': 'Resume already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except Resume.DoesNotExist:
            resume = Resume.objects.create(user=request.user)
            serializer = ResumeSerializer(resume)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def download_pdf(self, request, pk=None):
        """
        Download resume as PDF
        """
        # This would use a library like reportlab or weasyprint
        # For now, returning a placeholder response
        return Response({'message': 'PDF download functionality coming soon'}, status=status.HTTP_200_OK)


class ExperienceViewSet(viewsets.ModelViewSet):
    """
    Work experience management
    """
    serializer_class = ExperienceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Experience.objects.filter(resume__user=self.request.user)
    
    def perform_create(self, serializer):
        resume = self.request.user.resume
        serializer.save(resume=resume)


class EducationViewSet(viewsets.ModelViewSet):
    """
    Education management
    """
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Education.objects.filter(resume__user=self.request.user)
    
    def perform_create(self, serializer):
        resume = self.request.user.resume
        serializer.save(resume=resume)
