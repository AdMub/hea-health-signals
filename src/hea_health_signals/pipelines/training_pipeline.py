import sys
from src.hea_health_signals.components.data_ingestion import DataIngestion
from src.hea_health_signals.components.data_transformation import DataTransformation
from src.hea_health_signals.components.model_trainer import ModelTrainer

if __name__=="__main__":
    try:
        print("DEBUG: Pipeline started.")
        
        # 1. Ingest Data
        print("DEBUG: Starting Data Ingestion...")
        obj = DataIngestion()
        train_path, test_path = obj.initiate_data_ingestion()
        print(f"DEBUG: Data Ingestion Done.")

        # 2. Transform Data
        print("DEBUG: Starting Data Transformation...")
        data_transformation = DataTransformation()
        train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_path, test_path)
        print(f"DEBUG: Data Transformation Done.")

        # 3. Train Model
        print("DEBUG: Starting Model Trainer...")
        trainer = ModelTrainer()
        trainer.initiate_model_trainer(train_arr, test_arr)
        
        print("DEBUG: Training Pipeline Completed Successfully!")
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()