from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import AIInteraction
from .services import CareerAIAssistant
from .serializers import AIInteractionSerializer

class AIAssistantViewSet(viewsets.ModelViewSet):
    """
    AI Assistant endpoints
    """
    serializer_class = AIInteractionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return AIInteraction.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def job_insights(self, request):
        """
        Get AI insights about a job
        """
        job_name = request.data.get('job_name')
        if not job_name:
            return Response({'error': 'job_name required'}, status=status.HTTP_400_BAD_REQUEST)
        
        response = CareerAIAssistant.get_job_insights(job_name)
        
        # Log interaction
        interaction = AIInteraction.objects.create(
            user=request.user,
            interaction_type='job_insights',
            user_input=job_name,
            ai_response=response
        )
        
        serializer = AIInteractionSerializer(interaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def skill_gap_analysis(self, request):
        """
        Analyze skill gap
        """
        user_skills = request.data.get('user_skills', [])
        required_skills = request.data.get('required_skills', [])
        
        if not user_skills or not required_skills:
            return Response({'error': 'user_skills and required_skills required'}, status=status.HTTP_400_BAD_REQUEST)
        
        response = CareerAIAssistant.analyze_skill_gap(user_skills, required_skills)
        
        interaction = AIInteraction.objects.create(
            user=request.user,
            interaction_type='skill_gap',
            user_input=f"User: {user_skills}, Required: {required_skills}",
            ai_response=response
        )
        
        serializer = AIInteractionSerializer(interaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def interview_tips(self, request):
        """
        Get interview preparation tips
        """
        job_name = request.data.get('job_name')
        question = request.data.get('question')
        
        response = CareerAIAssistant.generate_interview_tips(job_name, question)
        
        interaction = AIInteraction.objects.create(
            user=request.user,
            interaction_type='interview_tips',
            user_input=question or job_name,
            ai_response=response
        )
        
        serializer = AIInteractionSerializer(interaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def resume_review(self, request):
        """
        AI Resume review
        """
        resume_text = request.data.get('resume')
        if not resume_text:
            return Response({'error': 'resume text required'}, status=status.HTTP_400_BAD_REQUEST)
        
        response = CareerAIAssistant.review_resume(resume_text)
        
        interaction = AIInteraction.objects.create(
            user=request.user,
            interaction_type='resume_review',
            user_input=resume_text[:200],  # Store only first 200 chars
            ai_response=response
        )
        
        serializer = AIInteractionSerializer(interaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rate_response(self, request, pk=None):
        """
        Rate AI response
        """
        interaction = self.get_object()
        rating = request.data.get('rating')
        feedback = request.data.get('feedback', '')
        
        if not rating or rating not in range(1, 6):
            return Response({'error': 'Rating must be between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)
        
        interaction.rating = rating
        interaction.feedback = feedback
        interaction.save()
        
        serializer = AIInteractionSerializer(interaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
