from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = "-e ."


def get_requirements(file_path: str) -> List[str]:
    """
    this function returns the list of requirements
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


setup(
    name="hea_health_signals",
    version="0.0.1",
    author="AdMub",
    author_email="admub465@gmail.com",
    description="A context-aware anomaly detection system for early health risk signals",
    # We need specific libraries for Health AI (NLP + Anomaly Detection)
    install_requires=get_requirements("requirements.txt"),
    packages=find_packages(),
)
