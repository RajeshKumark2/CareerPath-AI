from rest_framework import serializers
from .models import InterviewQuestion, MockTest, MockTestResponse

class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = ['question_id', 'job', 'question', 'question_type', 'difficulty', 
                  'answer_hint', 'suggested_answer', 'created_at']

class MockTestResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockTestResponse
        fields = ['id', 'mock_test', 'question', 'user_answer', 'is_correct', 'score', 'feedback']

class MockTestSerializer(serializers.ModelSerializer):
    responses = MockTestResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = MockTest
        fields = ['id', 'user', 'job', 'title', 'total_questions', 'duration_minutes', 
                  'passing_score', 'started_at', 'completed_at', 'is_completed', 'score', 'responses']
