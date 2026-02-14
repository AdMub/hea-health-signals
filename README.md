# HeaSphere | AI Health Orchestration Engine 🚑

[![CI/CD Pipeline](https://github.com/AdMub/hea-health-signals/actions/workflows/django.yml/badge.svg)](https://github.com/AdMub/hea-health-signals/actions)
![Python Version](https://img.shields.io/badge/Python-3.12-blue)
![Django Version](https://img.shields.io/badge/Django-5.0-green)
![Deployment](https://img.shields.io/badge/Deploy-Render-purple)

**HeaSphere** is an AI-powered **Health Logistics Operating System** designed to bridge the gap between "weak health signals" and professional medical intervention. 

Unlike standard symptom checkers, HeaSphere focuses on **Orchestration**: detecting non-obvious anomalies using XGBoost, explaining them via SHAP values, and physically routing emergency logistics (Ambulances) using geospatial intelligence.

---

### 🌐 Live Demo
**[Launch HeaSphere Dashboard](https://hea-sphere-live.onrender.com)**

> **⚠️ Note for Visitors:** This project is deployed on a **Free Tier** instance. The server "sleeps" when inactive.  
> **Please allow 1 minute for the initial wake-up** when you first click the link. It will be fast after that!

---

## 📸 System Demo

### 1. The Orchestration Dashboard
*Real-time risk monitoring with Explainable AI (SHAP) drivers.*
![Dashboard View](/images/dashboard_overview.png)
![Dashboard View](/images/dashboard_overview_2.png)


### 2. Live Logistics Dispatch (Leaflet.js)
*Automated ambulance routing triggered when risk > 60%.*
![Live Map Simulation](/images/live_map_dispatch.png)


---

## 🚀 Key Features

### 🧠 1. Context-Aware Anomaly Detection
Instead of static thresholds, HeaSphere analyzes **Velocity Variables** (e.g., how fast BMI is changing over 2 years) using an **XGBoost Regressor**. This allows us to catch "weak signals" before they become emergencies.

### 🔍 2. Explainable AI (XAI)
We don't trust "Black Boxes." The system uses **SHAP (SHapley Additive exPlanations)** to generate a dynamic bar chart for every prediction, showing exactly *why* the AI flagged a risk (e.g., "Age contributed +15%, but BP history contributed +40%").

### 🚑 3. Autonomous Logistics Dispatch
Built-in **Geo-Spatial Triage Engine**:
- **Low Risk:** System remains in "Passive Monitoring" mode.
- **High Risk (>60%):** Instantly triggers the **Leaflet.js** logistics layer, animating a live ambulance dispatch simulation from the nearest "Hea-Certified" facility to the patient's geolocated baseline.

### 🛡️ 4. Safety & Ethics "Air Gap"
- **Non-Diagnostic:** The AI never diagnoses. It flags anomalies and hands over to the **Hea Assistant**, which uses empathetic, non-clinical questioning to gather context for a human specialist.
- **Fairness Audit:** The model is audited for gender parity (39% Male / 33% Female risk distribution) to prevent algorithmic bias.

---

## 🛠️ Tech Stack

| Domain | Technology | Use Case |
| :--- | :--- | :--- |
| **Core Backend** | **Django 5.0 (Python)** | MVT Architecture, API Endpoints, Orchestration Logic |
| **ML Engine** | **XGBoost & CatBoost** | Anomaly Regression Model (PR-AUC 0.85) |
| **Explainability** | **SHAP** | Feature Importance Visualization |
| **Frontend** | **JavaScript & Tailwind** | Asynchronous Dashboard, Dynamic Gauges |
| **Geospatial** | **Leaflet.js & OpenStreetMap** | Interactive Maps, Routing Animation |
| **DevOps** | **Docker & GitHub Actions** | Containerization, CI/CD Automated Testing |
| **Deployment** | **Render Cloud** | Production Hosting with Gunicorn/WhiteNoise |

---

## ⚙️ Installation & Local Setup

Want to run the Orchestration Engine locally?

**1. Clone the Repository**
```bash
git clone [https://github.com/AdMub/hea-health-signals.git](https://github.com/AdMub/hea-health-signals.git)
cd hea-health-signals
```

### **2. Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```
### **5. Launch the System**
```bash
python manage.py runserver
Access the dashboard at http://127.0.0.1:8000/.
```


### **🧪 Testing the Simulation**
To see the **Emergency Dispatch Protocol** in action without waiting for real health data degradation:

1. Open the Dashboard.
2. Click the "Run Demo Scenario" link in the footer (or manually input BMI: 35, Health: 5, BP: High).
3. Watch the Risk Gauge turn red and the Ambulance physically navigate the map to the target zone.

📜 License & Credits
Author: [Your Name]

License: MIT License

Context: Developed for the Hea Health Hackathon (Focus: Context-Aware Health Signals).

### **👨‍💻 Author**

**Mubarak Adisa** *AI Engineer & Full-Stack Developer*

- 🎓 **Background:** Civil Engineering graduate transitioning into Computer Science, with a focus on Data Science & AI Systems.
- 🛠️ **Specialization:** Building orchestrated systems that bridge physical infrastructure (Logistics/Civil) with digital intelligence (AI/ML).
- 🔗 **GitHub:** [AdMub](https://github.com/AdMub)  
- 💼 **LinkedIn:** [Mubarak Adisa](https://www.linkedin.com/in/mubarak-adisa-334a441b6/)

---

### **📄 License**

Distributed under the **MIT License**. See `LICENSE` for more information.  
*(This project is open-source for educational and portfolio purposes.)*

---

### **🌟 Acknowledgements & Credits**

HeaSphere was built as a high-fidelity prototype to demonstrate **Context-Aware Health Orchestration**.

- **Inspiration:** Developed with the philosophy of the **Hea Health Hackathon** (Detecting "Weak Signals" before they become emergencies).
- **Geospatial Engine:** Powered by **Leaflet.js** and **OpenStreetMap** contributors for the live dispatch simulation.
- **Machine Learning:** Built on the shoulders of **XGBoost** and **SHAP** (slundberg/shap) for model explainability.
- **Infrastructure:** Deployed on **Render** Cloud; Backend powered by **Django Framework**.