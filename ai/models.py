from django.db import models
from django.contrib.auth.models import User
from jobs.models import JobRole

class AIInteraction(models.Model):
    """
    Log AI interactions for analytics and improvement
    """
    INTERACTION_TYPE_CHOICES = [
        ('job_insights', 'Job Insights'),
        ('skill_gap', 'Skill Gap Analysis'),
        ('interview_tips', 'Interview Tips'),
        ('resume_review', 'Resume Review'),
        ('career_recommendation', 'Career Recommendation'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_interactions')
    interaction_type = models.CharField(max_length=50, choices=INTERACTION_TYPE_CHOICES)
    job = models.ForeignKey(JobRole, on_delete=models.SET_NULL, null=True, blank=True)
    user_input = models.TextField()
    ai_response = models.TextField()
    rating = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])
    feedback = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.interaction_type}"
    
    class Meta:
        ordering = ['-created_at']
