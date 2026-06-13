from django.db import models
from django.contrib.auth.models import User
from jobs.models import JobRole

class InterviewQuestion(models.Model):
    """
    Interview questions for job roles
    """
    QUESTION_TYPE_CHOICES = [
        ('technical', 'Technical'),
        ('hr', 'HR/Behavioral'),
        ('situational', 'Situational'),
    ]
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    question_id = models.AutoField(primary_key=True)
    job = models.ForeignKey(JobRole, on_delete=models.CASCADE, related_name='interview_questions')
    question = models.TextField()
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    answer_hint = models.TextField(blank=True)
    suggested_answer = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.job.job_name} - {self.question[:50]}"
    
    class Meta:
        ordering = ['difficulty', 'question_type']


class MockTest(models.Model):
    """
    Mock test for interview preparation
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mock_tests')
    job = models.ForeignKey(JobRole, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    total_questions = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=60)  # in minutes
    passing_score = models.FloatField(default=60)
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    score = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    class Meta:
        ordering = ['-started_at']


class MockTestResponse(models.Model):
    """
    User's response to mock test questions
    """
    mock_test = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE)
    user_answer = models.TextField()
    is_correct = models.BooleanField(null=True, blank=True)
    score = models.FloatField(default=0)
    feedback = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.mock_test.user.username} - Q{self.question.question_id}"
