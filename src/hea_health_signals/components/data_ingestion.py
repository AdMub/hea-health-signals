import os
import sys
import pandas as pd
import numpy as np
from src.hea_health_signals.exception import CustomException
from src.hea_health_signals.logger import logging
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "rand_cleaned.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Starting Real Data Ingestion (RAND HRS)")
        try:
            # 1. PATH CONFIGURATION
            # Checks for dataset in multiple likely locations
            possible_paths = [
                r"Datasets\randhrs1992_2022v1.dta",
                r"..\Datasets\randhrs1992_2022v1.dta",
                r"../Datasets/randhrs1992_2022v1.dta"
            ]
            
            dta_path = None
            for p in possible_paths:
                if os.path.exists(p):
                    dta_path = p
                    break
            
            if dta_path is None:
                raise FileNotFoundError(f"Could not find RAND file in: {possible_paths}")

            logging.info(f"Reading .dta file from {dta_path}...")
            
            # 2. LOAD SPECIFIC COLUMNS (For Feature Engineering)
            cols_to_use = [
                'hhidpn', 
                'r11diab', 'r10diab',      # Target (2012) & History (2010)
                'r10bmi', 'r9bmi',         # BMI (2010 vs 2008)
                'r10shlt', 'r9shlt',       # Self-Rated Health
                'r10cesd', 'r9cesd',       # Depression Score
                'r10hibp',                 # Blood Pressure
                'r10agey_e',               # Age
                'r10smokev',               # Smoking
                'r10drink',                # Alcohol
                'ragender'                 # Gender (for Fairness)
            ]
            
            # Load without converting categories (keep as numbers)
            df = pd.read_stata(dta_path, columns=cols_to_use, convert_categoricals=False)

            # 3. FILTERING: "The Hidden Signal"
            # We only train on people who were HEALTHY (0) in 2010
            # We want to predict who GETS SICK (1) in 2012
            df_clean = df[df['r10diab'] == 0].copy()
            logging.info(f"Healthy Population (2010): {df_clean.shape[0]}")

            # 4. ROBUST FEATURE ENGINEERING
            # A. Ratios (Better than subtraction for scaling)
            # Add small epsilon (0.1) to avoid divide by zero
            df_clean['r9bmi'] = df_clean['r9bmi'].fillna(df_clean['r10bmi']) # Fill missing history
            df_clean['bmi_ratio'] = df_clean['r10bmi'] / (df_clean['r9bmi'] + 0.1)
            
            # B. Health Decline (Worsening perception)
            # r10shlt is 1-5 (5 is Poor). Positive diff = Worsening health.
            df_clean['r9shlt'] = df_clean['r9shlt'].fillna(df_clean['r10shlt'])
            df_clean['health_decline'] = df_clean['r10shlt'] - df_clean['r9shlt']
            
            # C. Mental Health Shift
            df_clean['r9cesd'] = df_clean['r9cesd'].fillna(df_clean['r10cesd'])
            df_clean['cesd_change'] = df_clean['r10cesd'] - df_clean['r9cesd']
            
            # D. Interaction Terms (High Impact for XGBoost)
            df_clean['age_bmi_interact'] = df_clean['r10agey_e'] * df_clean['r10bmi']
            df_clean['bp_bmi_interact'] = df_clean['r10hibp'] * df_clean['r10bmi'] # The "Deadly Duo"
            df_clean['psycho_somatic'] = df_clean['r10cesd'] * df_clean['r10shlt'] # Depression + Physical Pain

            # 5. CLEANUP
            # Must have a target in 2012
            df_clean = df_clean.dropna(subset=['r11diab'])
            df_clean = df_clean.fillna(0) # Simple imputation for remaining gaps

            # 6. SAVE ARTIFACTS
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            
            # Stratified Split (Keep sick ratio same in train/test)
            from sklearn.model_selection import train_test_split
            train_df, test_df = train_test_split(df_clean, test_size=0.2, random_state=42, stratify=df_clean['r11diab'])

            train_df.to_csv(self.ingestion_config.train_data_path, index=False)
            test_df.to_csv(self.ingestion_config.test_data_path, index=False)

            logging.info(f"Ingestion Complete. Train: {train_df.shape}, Test: {test_df.shape}")
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)