from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import os

# Ensure we can find the src folder
sys.path.append(os.getcwd())
from src.hea_health_signals.pipelines.prediction_pipeline import PredictPipeline

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def analyze_signals(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pipeline = PredictPipeline()
            result = pipeline.predict(data)
            
            # 1. Add Multi-Domain Risk scoring (Requirement)
            result['categories'] = {
                'metabolic': round(result['risk_score'] * 100, 1),
                'psycho_emotional': round(float(data['depression_current']) * 12.5, 1),
                'cardiovascular': 75.0 if int(data['high_bp']) == 1 else 20.0
            }
            
            # 2. Add Empathetic Follow-up (Requirement)
            result['follow_up'] = pipeline.get_empathetic_followup(result, data)
            
            return JsonResponse({'status': 'success', 'analysis': result})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)