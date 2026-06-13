from rest_framework import serializers
from .models import JobRole, Skill, Tool, SalaryInsight, JobProcess, CareerGrowthPath

class JobRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRole
        fields = ['job_id', 'job_name', 'description', 'overview', 'work_summary', 'created_at', 'updated_at']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['skill_id', 'skill_name', 'skill_type', 'description', 'proficiency_level']

class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'tool_name', 'description', 'usage']

class SalaryInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryInsight
        fields = ['job', 'fresher_salary_min', 'fresher_salary_max', 'mid_salary_min', 
                  'mid_salary_max', 'senior_salary_min', 'senior_salary_max', 'currency']

class JobProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProcess
        fields = ['job', 'process_json']

class CareerGrowthPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerGrowthPath
        fields = ['job', 'growth_json']
