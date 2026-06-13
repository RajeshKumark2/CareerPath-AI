from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from jobs.models import JobRole
from .models import InterviewQuestion, MockTest, MockTestResponse
from .serializers import InterviewQuestionSerializer, MockTestSerializer, MockTestResponseSerializer
from django.utils import timezone

class InterviewQuestionViewSet(viewsets.ModelViewSet):
    """
    Interview question management
    """
    queryset = InterviewQuestion.objects.all()
    serializer_class = InterviewQuestionSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def by_job(self, request):
        """
        Get interview questions for a specific job
        """
        job_id = request.query_params.get('job_id')
        question_type = request.query_params.get('type')
        
        queries = InterviewQuestion.objects.filter(job_id=job_id)
        if question_type:
            queries = queries.filter(question_type=question_type)
        
        serializer = InterviewQuestionSerializer(queries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MockTestViewSet(viewsets.ModelViewSet):
    """
    Mock test management
    """
    serializer_class = MockTestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return MockTest.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def start(self, request):
        """
        Start a new mock test
        """
        job_id = request.data.get('job_id')
        try:
            job = JobRole.objects.get(job_id=job_id)
            mock_test = MockTest.objects.create(
                user=request.user,
                job=job,
                title=f"Mock Test - {job.job_name}",
                total_questions=10
            )
            serializer = MockTestSerializer(mock_test)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except JobRole.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def submit_answer(self, request, pk=None):
        """
        Submit answer to a question
        """
        mock_test = self.get_object()
        question_id = request.data.get('question_id')
        user_answer = request.data.get('answer')
        
        try:
            question = InterviewQuestion.objects.get(question_id=question_id)
            response, created = MockTestResponse.objects.get_or_create(
                mock_test=mock_test,
                question=question,
                defaults={'user_answer': user_answer}
            )
            if not created:
                response.user_answer = user_answer
                response.save()
            
            serializer = MockTestResponseSerializer(response)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except InterviewQuestion.DoesNotExist:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def complete(self, request, pk=None):
        """
        Complete the mock test
        """
        mock_test = self.get_object()
        mock_test.is_completed = True
        mock_test.completed_at = timezone.now()
        
        # Calculate score
        responses = mock_test.responses.all()
        if responses.count() > 0:
            total_score = sum([r.score for r in responses])
            mock_test.score = (total_score / responses.count()) * 100
        
        mock_test.save()
        serializer = MockTestSerializer(mock_test)
        return Response(serializer.data, status=status.HTTP_200_OK)
