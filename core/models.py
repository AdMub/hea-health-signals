from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# --- 1. CORE USER & ACCESS CONTROL ---
class User(AbstractUser):
    """
    Advanced User Model for Hea Orchestration.
    Distinguishes between patients and verified practitioners.
    """
    is_patient = models.BooleanField(default=True)
    is_practitioner = models.BooleanField(default=False)
    # Unique ID for secure, anonymized medical referencing
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.username} ({'Practitioner' if self.is_practitioner else 'Patient'})"

# --- 2. THE "WEAK SIGNAL" DETECTION LAYER ---
class HealthLog(models.Model):
    """
    Captures anomalies compared against the person's own baseline.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="logs")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Quantitative Signals (From your XGBoost Features)
    bmi_current = models.FloatField(null=True, blank=True)
    health_perception = models.IntegerField(null=True, blank=True) # 1-5 Scale
    depression_index = models.IntegerField(null=True, blank=True) # 0-8 Scale
    
    # Qualitative "Everyday Language" Input
    raw_text = models.TextField(help_text="Context-aware diary input for anomaly detection.")
    typing_speed_wpm = models.IntegerField(null=True, blank=True) # Digital Biomarker

    def __str__(self):
        return f"Log: {self.user.username} @ {self.timestamp.strftime('%H:%M')}"

class AnomalyResult(models.Model):
    """
    Multi-domain risk categorization.
    Stores AI analysis and prevents automated diagnosis.
    """
    RISK_DOMAINS = [
        ('METABOLIC', 'Metabolic Risk'),
        ('CARDIO', 'Cardiovascular'),
        ('PSYCHO', 'Psycho-Emotional'),
        ('NEURO', 'Neurological'),
        ('NONE', 'Stable')
    ]
    log = models.OneToOneField(HealthLog, on_delete=models.CASCADE, related_name="analysis")
    risk_score = models.FloatField(help_text="Anomaly score (0.0 - 1.0)")
    domain = models.CharField(max_length=20, choices=RISK_DOMAINS, default='NONE')
    
    # Explainability & Safety
    signal_explanation = models.TextField(help_text="The 'Why' behind the flag.")
    ai_followup_question = models.TextField(help_text="Safe, empathetic context-gathering question.")
    is_emergency = models.BooleanField(default=False) # Triggers Ambulance Logic

# --- 3. GEO-LOGISTICS & TRIAGE ENGINE ---
class MedicalFacility(models.Model):
    """
    Intelligent Triage Engine.
    Filters hospitals by specialty and live capacity.
    """
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=AnomalyResult.RISK_DOMAINS)
    latitude = models.FloatField()
    longitude = models.FloatField()
    specialties = models.JSONField(default=list) # e.g., ["Endocrinology", "ER"]
    is_certified = models.BooleanField(default=True) # "Hea-Certified" Specialist
    
    capacity_status = models.CharField(
        max_length=20, 
        choices=[('LOW', 'Low Wait'), ('MED', 'Medium'), ('HIGH', 'Crowded')],
        default='LOW'
    )

    def __str__(self):
        return f"{self.name} - {self.category}"

class Ambulance(models.Model):
    """
    Live Fleet Tracker.
    Tracks vehicle movement toward emergency anomaly events.
    """
    vehicle_id = models.CharField(max_length=50, unique=True)
    current_lat = models.FloatField()
    current_lng = models.FloatField()
    status = models.CharField(
        max_length=20, 
        choices=[('AVAILABLE', 'Available'), ('DISPATCHED', 'On Route')],
        default='AVAILABLE'
    )

    def __str__(self):
        return f"Ambulance {self.vehicle_id} ({self.status})"