from rest_framework import serializers
from .models import User, HealthLog, AnomalyResult, MedicalFacility, HealingCircle

class AnomalyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnomalyResult
        fields = ['risk_score', 'detected_category', 'signal_explanation', 'ai_empathy_response']

class HealthLogSerializer(serializers.ModelSerializer):
    # We include the analysis result inside the log response
    analysis = AnomalyResultSerializer(source='anomalyresult', read_only=True)
    
    class Meta:
        model = HealthLog
        fields = ['id', 'timestamp', 'raw_text', 'typing_speed_wpm', 'local_weather', 'analysis']

class MedicalFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalFacility
        fields = '__all__'