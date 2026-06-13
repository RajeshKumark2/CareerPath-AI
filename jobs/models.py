from django.db import models

class JobRole(models.Model):
    """
    Job role information
    """
    job_id = models.AutoField(primary_key=True)
    job_name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    overview = models.TextField(blank=True)
    work_summary = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.job_name
    
    class Meta:
        verbose_name = 'Job Role'
        verbose_name_plural = 'Job Roles'
        ordering = ['job_name']


class JobProcess(models.Model):
    """
    Job workflow/process steps
    """
    job = models.OneToOneField(JobRole, on_delete=models.CASCADE, related_name='process')
    process_json = models.JSONField(default=list)
    # Example: [{"step": 1, "name": "Business Requirement", "description": "..."}, ...]
    
    def __str__(self):
        return f"{self.job.job_name} - Process"


class Skill(models.Model):
    """
    Skills required for a job
    """
    SKILL_TYPE_CHOICES = [
        ('technical', 'Technical Skill'),
        ('soft', 'Soft Skill'),
        ('certification', 'Certification'),
    ]
    
    skill_id = models.AutoField(primary_key=True)
    job = models.ForeignKey(JobRole, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=200)
    skill_type = models.CharField(max_length=50, choices=SKILL_TYPE_CHOICES)
    description = models.TextField(blank=True)
    proficiency_level = models.CharField(
        max_length=20,
        choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')],
        default='intermediate'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.skill_name} - {self.job.job_name}"
    
    class Meta:
        unique_together = ['job', 'skill_name']
        ordering = ['skill_type', 'skill_name']


class Tool(models.Model):
    """
    Tools used in a job role
    """
    job = models.ForeignKey(JobRole, on_delete=models.CASCADE, related_name='tools')
    tool_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    usage = models.CharField(max_length=500, blank=True)
    
    def __str__(self):
        return f"{self.tool_name} - {self.job.job_name}"
    
    class Meta:
        unique_together = ['job', 'tool_name']
        ordering = ['tool_name']


class SalaryInsight(models.Model):
    """
    Salary information for job roles
    """
    LEVEL_CHOICES = [
        ('fresher', 'Fresher'),
        ('mid', 'Mid-Level'),
        ('senior', 'Senior-Level'),
        ('lead', 'Lead/Manager'),
    ]
    
    job = models.OneToOneField(JobRole, on_delete=models.CASCADE, related_name='salary')
    fresher_salary_min = models.FloatField(default=0)
    fresher_salary_max = models.FloatField(default=0)
    mid_salary_min = models.FloatField(default=0)
    mid_salary_max = models.FloatField(default=0)
    senior_salary_min = models.FloatField(default=0)
    senior_salary_max = models.FloatField(default=0)
    currency = models.CharField(max_length=3, default='INR')
    
    def __str__(self):
        return f"{self.job.job_name} - Salary"


class CareerGrowthPath(models.Model):
    """
    Career growth progression for a role
    """
    job = models.OneToOneField(JobRole, on_delete=models.CASCADE, related_name='growth_path')
    growth_json = models.JSONField(default=list)
    # Example: [{"level": 1, "position": "Data Analyst", "years": "0-2"}, ...]
    
    def __str__(self):
        return f"{self.job.job_name} - Career Growth"
