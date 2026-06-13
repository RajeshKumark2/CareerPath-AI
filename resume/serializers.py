from rest_framework import serializers
from .models import Resume, Experience, Education, ResumeSkill, Certification

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'job_title', 'company', 'employment_type', 'location', 
                  'start_date', 'end_date', 'is_current', 'description']

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'school', 'degree', 'field_of_study', 'start_date', 
                  'end_date', 'grade', 'description']

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['id', 'certification_name', 'issuing_organization', 'issue_date', 
                  'expiration_date', 'credential_url']

class ResumeSerializer(serializers.ModelSerializer):
    experiences = ExperienceSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    certifications = CertificationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Resume
        fields = ['id', 'template', 'professional_headline', 'summary', 'phone', 'location', 
                  'website', 'linkedin', 'github', 'experiences', 'educations', 'certifications', 
                  'created_at', 'updated_at']
