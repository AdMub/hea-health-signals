import sys
import os
import pandas as pd
import numpy as np
import joblib
from src.hea_health_signals.exception import CustomException

class PredictPipeline:
    def __init__(self):
        self.model_path = os.path.join('artifacts', 'model.pkl')
        self.thresh_path = os.path.join('artifacts', 'threshold.txt')
        self.preprocessor_path = os.path.join('artifacts', 'preprocessor.pkl')
        
        self.model = joblib.load(self.model_path)
        self.preprocessor = joblib.load(self.preprocessor_path)

        if os.path.exists(self.thresh_path):
            with open(self.thresh_path, 'r') as f:
                self.threshold = float(f.read().strip())
        else:
            self.threshold = 0.33

    def predict(self, input_data):
        try:
            r10bmi = float(input_data.get('bmi_current'))
            r9bmi = float(input_data.get('bmi_past')) 
            r10shlt = float(input_data.get('health_current')) 
            r9shlt = float(input_data.get('health_past'))
            r10cesd = float(input_data.get('depression_current')) 
            r9cesd = float(input_data.get('depression_past'))
            r10hibp = int(input_data.get('high_bp')) 
            r10agey_e = float(input_data.get('age'))

            bmi_ratio = r10bmi / (r9bmi + 0.1)
            health_decline = r10shlt - r9shlt
            cesd_change = r10cesd - r9cesd
            age_bmi_interact = r10agey_e * r10bmi
            bp_bmi_interact = r10hibp * r10bmi
            psycho_somatic = r10cesd * r10shlt
            
            data_dict = {
                'r10bmi': [r10bmi], 'bmi_ratio': [bmi_ratio], 'r10shlt': [r10shlt],
                'health_decline': [health_decline], 'r10cesd': [r10cesd], 'cesd_change': [cesd_change],
                'r10hibp': [r10hibp], 'r10agey_e': [r10agey_e], 'age_bmi_interact': [age_bmi_interact],
                'bp_bmi_interact': [bp_bmi_interact], 'psycho_somatic': [psycho_somatic]
            }
            
            df = pd.DataFrame(data_dict)
            data_scaled = self.preprocessor.transform(df)
            probs = self.model.predict_proba(data_scaled)[:, 1]
            risk_score = probs[0]
            is_risky = risk_score >= self.threshold
            
            return {
                "is_risky": bool(is_risky),
                "risk_score": float(risk_score),
                "threshold_used": self.threshold
            }
        except Exception as e:
            raise CustomException(e, sys)

    def get_empathetic_followup(self, analysis_results, inputs):
        """Meets the Hackathon 'Safe Follow-up' requirement."""
        if float(inputs.get('bmi_current')) > float(inputs.get('bmi_past')):
            return "I've noticed a non-obvious pattern in your metabolic velocity. Have you experienced any persistent fatigue or changes in your thirst levels after meals recently?"
        elif float(inputs.get('health_current')) > float(inputs.get('health_past')):
            return "The data shows a slight shift in your subjective health baseline. Has your sleep quality or stress level changed significantly over the last few months?"
        return "Your current signals appear stable compared to your personal baseline. Is there anything specific about your energy levels you'd like to track today?"