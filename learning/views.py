from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from jobs.models import JobRole
from .models import LearningRoadmap, UserLearningProgress, LearningResource
from .serializers import LearningRoadmapSerializer, UserLearningProgressSerializer, LearningResourceSerializer

class LearningRoadmapViewSet(viewsets.ModelViewSet):
    """
    Learning roadmap management
    """
    queryset = LearningRoadmap.objects.all()
    serializer_class = LearningRoadmapSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def by_job(self, request):
        """
        Get learning roadmap for a specific job
        """
        job_id = request.query_params.get('job_id')
        if job_id:
            try:
                roadmap = LearningRoadmap.objects.get(job_id=job_id)
                serializer = LearningRoadmapSerializer(roadmap)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except LearningRoadmap.DoesNotExist:
                return Response({'error': 'Roadmap not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'job_id parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def resources(self, request, pk=None):
        """
        Get resources for a roadmap
        """
        roadmap = self.get_object()
        resources = roadmap.resources.all()
        serializer = LearningResourceSerializer(resources, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserLearningProgressViewSet(viewsets.ModelViewSet):
    """
    User learning progress tracking
    """
    serializer_class = UserLearningProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserLearningProgress.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def start_roadmap(self, request):
        """
        Start a learning roadmap
        """
        roadmap_id = request.data.get('roadmap_id')
        try:
            roadmap = LearningRoadmap.objects.get(roadmap_id=roadmap_id)
            progress, created = UserLearningProgress.objects.get_or_create(
                user=request.user,
                roadmap=roadmap
            )
            serializer = UserLearningProgressSerializer(progress)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        except LearningRoadmap.DoesNotExist:
            return Response({'error': 'Roadmap not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['put'], permission_classes=[IsAuthenticated])
    def update_progress(self, request, pk=None):
        """
        Update learning progress
        """
        progress = self.get_object()
        serializer = UserLearningProgressSerializer(progress, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
