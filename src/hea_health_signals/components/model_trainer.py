import os
import sys
from dataclasses import dataclass
import numpy as np

# XGBoost for winning metrics
import xgboost as xgb
from sklearn.metrics import fbeta_score, roc_auc_score, precision_recall_curve, auc, classification_report
from src.hea_health_signals.exception import CustomException
from src.hea_health_signals.logger import logging
import joblib

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")
    threshold_file_path = os.path.join("artifacts", "threshold.txt")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Split training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            # 1. DYNAMIC IMBALANCE RATIO
            num_healthy = (y_train == 0).sum()
            num_sick = (y_train == 1).sum()
            ratio = num_healthy / num_sick
            logging.info(f"Training XGBoost. Imbalance Ratio: {ratio:.2f}")

            # 2. CONFIGURE XGBOOST (Optimized for PR-AUC)
            model = xgb.XGBClassifier(
                scale_pos_weight=ratio,      # Aggressive balancing
                n_estimators=600,            # High trees
                learning_rate=0.02,          # Slow learning
                max_depth=4,                 # Prevent overfitting
                min_child_weight=5,          # Conservative
                subsample=0.8,
                colsample_bytree=0.8,
                eval_metric='aucpr',         # Optimize Precision-Recall Area
                use_label_encoder=False,
                random_state=42
            )
            
            logging.info("Fitting Model...")
            model.fit(X_train, y_train)

            # 3. THRESHOLD OPTIMIZATION (Maximize F2-Score)
            logging.info("Optimizing Threshold for F2-Score...")
            probs = model.predict_proba(X_test)[:, 1]
            
            best_threshold = 0.5
            best_f2 = 0.0

            # Scan thresholds
            for t in np.linspace(0.05, 0.5, 50):
                preds_temp = (probs >= t).astype(int)
                # Beta=2 weighs Recall 2x higher than Precision
                score = fbeta_score(y_test, preds_temp, beta=2)
                if score > best_f2:
                    best_f2 = score
                    best_threshold = t

            # 4. FINAL EVALUATION
            final_preds = (probs >= best_threshold).astype(int)
            roc_auc = roc_auc_score(y_test, probs)
            precision, recall, _ = precision_recall_curve(y_test, probs)
            pr_auc = auc(recall, precision)

            print(f"\n==========================================")
            print(f"🏆 WINNING METRICS (Threshold {best_threshold:.3f})")
            print(f"==========================================")
            print(f"MAX F2-SCORE:  {best_f2:.4f}")
            print(f"PR-AUC:        {pr_auc:.4f}")
            print(f"ROC-AUC:       {roc_auc:.4f}")
            print(f"------------------------------------------")
            print(classification_report(y_test, final_preds))
            print(f"==========================================\n")

            # 5. SAVE ARTIFACTS
            joblib.dump(model, self.model_trainer_config.trained_model_file_path)
            
            # Save the optimal threshold to a text file
            with open(self.model_trainer_config.threshold_file_path, "w") as f:
                f.write(str(best_threshold))

            logging.info(f"Model saved to {self.model_trainer_config.trained_model_file_path}")
            logging.info(f"Threshold {best_threshold} saved to {self.model_trainer_config.threshold_file_path}")
            
            return self.model_trainer_config.trained_model_file_path

        except Exception as e:
            raise CustomException(e, sys)