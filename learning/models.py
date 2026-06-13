from django.db import models
from django.contrib.auth.models import User
from jobs.models import JobRole

class LearningRoadmap(models.Model):
    """
    Learning roadmap for a job role
    """
    roadmap_id = models.AutoField(primary_key=True)
    job = models.OneToOneField(JobRole, on_delete=models.CASCADE, related_name='roadmap')
    roadmap_json = models.JSONField(default=list)
    # Example: [{"step": 1, "skill": "Excel", "duration": "1 month", "resources": [...]}, ...]
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.job.job_name} - Roadmap"


class UserLearningProgress(models.Model):
    """
    Track user's learning progress
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_progress')
    roadmap = models.ForeignKey(LearningRoadmap, on_delete=models.CASCADE)
    current_step = models.IntegerField(default=0)
    completed_steps = models.IntegerField(default=0)
    progress_percentage = models.FloatField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.roadmap.job.job_name}"
    
    class Meta:
        unique_together = ['user', 'roadmap']


class LearningResource(models.Model):
    """
    Learning resources (courses, books, tutorials)
    """
    RESOURCE_TYPE_CHOICES = [
        ('course', 'Online Course'),
        ('book', 'Book'),
        ('tutorial', 'Tutorial'),
        ('video', 'Video'),
        ('project', 'Project'),
    ]
    
    roadmap = models.ForeignKey(LearningRoadmap, on_delete=models.CASCADE, related_name='resources')
    step_number = models.IntegerField()
    resource_name = models.CharField(max_length=300)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPE_CHOICES)
    url = models.URLField()
    description = models.TextField(blank=True)
    duration = models.CharField(max_length=100, blank=True)  # e.g., "2 hours", "4 weeks"
    difficulty_level = models.CharField(
        max_length=20,
        choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')],
        default='beginner'
    )
    is_free = models.BooleanField(default=True)
    price = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.resource_name} - Step {self.step_number}"
    
    class Meta:
        ordering = ['step_number', 'difficulty_level']
