from django.contrib import admin
from .models import User, HealthLog, AnomalyResult, MedicalFacility, Ambulance

@admin.register(MedicalFacility)
class MedicalFacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'capacity_status', 'is_certified')
    list_filter = ('category', 'capacity_status', 'is_certified')
    search_fields = ('name', 'specialties')
    # Helps you place hospitals on the map manually for the demo
    fieldsets = (
        ('Basic Info', {'fields': ('name', 'category', 'is_certified')}),
        ('Location Data', {'fields': ('latitude', 'longitude')}),
        ('Live Operations', {'fields': ('specialties', 'capacity_status')}),
    )

@admin.register(Ambulance)
class AmbulanceAdmin(admin.ModelAdmin):
    list_display = ('vehicle_id', 'status', 'current_lat', 'current_lng')
    list_editable = ('status',)

@admin.register(AnomalyResult)
class AnomalyResultAdmin(admin.ModelAdmin):
    list_display = ('domain', 'risk_score', 'is_emergency')
    readonly_fields = ('risk_score', 'domain', 'signal_explanation')