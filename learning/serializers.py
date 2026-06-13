from rest_framework import serializers
from .models import LearningRoadmap, UserLearningProgress, LearningResource

class LearningResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningResource
        fields = ['id', 'step_number', 'resource_name', 'resource_type', 'url', 
                  'description', 'duration', 'difficulty_level', 'is_free', 'price']

class LearningRoadmapSerializer(serializers.ModelSerializer):
    resources = LearningResourceSerializer(many=True, read_only=True)
    
    class Meta:
        model = LearningRoadmap
        fields = ['roadmap_id', 'job', 'roadmap_json', 'resources', 'created_at', 'updated_at']

class UserLearningProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLearningProgress
        fields = ['id', 'user', 'roadmap', 'current_step', 'completed_steps', 
                  'progress_percentage', 'started_at', 'updated_at']
