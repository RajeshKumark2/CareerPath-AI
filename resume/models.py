from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    """
    User resume
    """
    TEMPLATE_CHOICES = [
        ('classic', 'Classic ATS-Friendly'),
        ('modern', 'Modern'),
        ('creative', 'Creative'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')
    template = models.CharField(max_length=50, choices=TEMPLATE_CHOICES, default='classic')
    
    # Personal Info
    professional_headline = models.CharField(max_length=200, blank=True)
    summary = models.TextField(blank=True)
    
    # Contact
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - Resume"


class Experience(models.Model):
    """
    Work experience
    """
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    employment_type = models.CharField(
        max_length=50,
        choices=[
            ('full-time', 'Full-time'),
            ('part-time', 'Part-time'),
            ('internship', 'Internship'),
            ('contract', 'Contract'),
        ]
    )
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.job_title} at {self.company}"


class Education(models.Model):
    """
    Education details
    """
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='educations')
    school = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    grade = models.CharField(max_length=10, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-end_date']
    
    def __str__(self):
        return f"{self.degree} in {self.field_of_study}"


class ResumeSkill(models.Model):
    """
    Skills on resume
    """
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=200)
    proficiency = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert'),
        ],
        default='intermediate'
    )
    
    class Meta:
        unique_together = ['resume', 'skill_name']
    
    def __str__(self):
        return f"{self.skill_name} - {self.proficiency}"


class Certification(models.Model):
    """
    Certifications
    """
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certifications')
    certification_name = models.CharField(max_length=300)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    credential_url = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.certification_name}"
