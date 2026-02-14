import sys
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import joblib
from dataclasses import dataclass
from src.hea_health_signals.exception import CustomException
from src.hea_health_signals.logger import logging

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            # EXACT FEATURES FROM INGESTION
            numerical_columns = [
                'r10bmi', 
                'bmi_ratio', 
                'r10shlt', 
                'health_decline',
                'r10cesd', 
                'cesd_change', 
                'r10hibp', 
                'r10agey_e', 
                'age_bmi_interact', 
                'bp_bmi_interact', 
                'psycho_somatic'
            ]
            
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns)
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
            
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Obtaining preprocessing object")
            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "r11diab"
            
            # Explicit Feature Selection to avoid column mismatch errors
            feature_cols = [
                'r10bmi', 'bmi_ratio', 'r10shlt', 'health_decline',
                'r10cesd', 'cesd_change', 'r10hibp', 'r10agey_e', 
                'age_bmi_interact', 'bp_bmi_interact', 'psycho_somatic'
            ]
            
            input_feature_train_df = train_df[feature_cols]
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df[feature_cols]
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            os.makedirs(os.path.dirname(self.data_transformation_config.preprocessor_obj_file_path), exist_ok=True)
            joblib.dump(preprocessing_obj, self.data_transformation_config.preprocessor_obj_file_path)

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
            
        except Exception as e:
            raise CustomException(e, sys)