import os
import sys
import joblib
import pandas as pd
from sklearn.metrics import classification_report, fbeta_score
from src.hea_health_signals.exception import CustomException
from src.hea_health_signals.logger import logging

class ModelEvaluation:
    def __init__(self):
        pass

    def initiate_model_evaluation(self, train_array, test_array):
        try:
            logging.info("Loading Model and Threshold...")
            model_path = os.path.join("artifacts", "model.pkl")
            thresh_path = os.path.join("artifacts", "threshold.txt")
            
            model = joblib.load(model_path)
            with open(thresh_path, 'r') as f:
                threshold = float(f.read().strip())

            X_test = test_array[:, :-1]
            y_test = test_array[:, -1]

            probs = model.predict_proba(X_test)[:, 1]
            preds = (probs >= threshold).astype(int)

            f2 = fbeta_score(y_test, preds, beta=2)
            logging.info(f"Independent Evaluation F2-Score: {f2}")
            print(f"Independent Eval F2: {f2}")

        except Exception as e:
            raise CustomException(e, sys)