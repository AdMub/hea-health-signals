import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s:")

project_name = "hea_health_signals"

list_of_files = [
    ".github/workflows/.gitkeep",
    # Source Code Structure
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/components/data_ingestion.py",  # For reading user logs
    f"src/{project_name}/components/data_transformation.py",  # For NLP/Vectorization
    f"src/{project_name}/components/model_trainer.py",  # For Isolation Forest
    f"src/{project_name}/components/model_evaluation.py",  # For Risk Scoring
    f"src/{project_name}/pipelines/__init__.py",
    f"src/{project_name}/pipelines/training_pipeline.py",
    f"src/{project_name}/pipelines/prediction_pipeline.py",  # Real-time anomaly check
    f"src/{project_name}/logger.py",
    f"src/{project_name}/exception.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    # Web App Structure (Django/Flask/Streamlit)
    "app.py",  # Entry point
    "templates/index.html",
    "static/css/style.css",
    # Config & DevOps
    "config/config.yaml",
    "params.yaml",
    "dvc.yaml",  # If you use DVC for data versioning
    "Dockerfile",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb",  # Renamed from experiment for clarity
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} is already exists")
