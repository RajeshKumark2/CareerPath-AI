from rest_framework import serializers
from .models import AIInteraction

class AIInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIInteraction
        fields = ['id', 'user', 'interaction_type', 'job', 'user_input', 'ai_response', 
                  'rating', 'feedback', 'created_at']
