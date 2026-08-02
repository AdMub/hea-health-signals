

# HeaSphere | Motor de Orquestación de Salud con IA 🚑

[![Canal de CI/CD](https://github.com/AdMub/hea-health-signals/actions/workflows/django.yml/badge.svg)](https://github.com/AdMub/hea-health-signals/actions)
![Versión de Python](https://img.shields.io/badge/Python-3.12-blue)
![Versión de Django](https://img.shields.io/badge/Django-5.0-green)
![Despliegue](https://img.shields.io/badge/Deploy-Render-purple)

**HeaSphere** es un **Sistema Operativo de Logística de Salud** impulsado por IA, diseñado para cerrar la brecha entre las "señales débiles de salud" y la intervención médica profesional. 

A diferencia de los revisores de síntomas estándar, HeaSphere se centra en la **Orquestación**: detectar anomalías no obvias utilizando XGBoost, explicarlas mediante valores SHAP y enrutar físicamente la logística de emergencias (Ambulancias) utilizando inteligencia geoespacial.

---

### 🌐 Demo en Vivo
**[Iniciar Panel de HeaSphere](https://hea-sphere-live.onrender.com)**

> **⚠️ Nota para visitantes:** Este proyecto se despliega en una instancia de **Nivel Gratuito (Free Tier)**. El servidor "dorma" cuando está inactivo.  
> **Espere 1 minuto para el arranque inicial** al hacer clic en el enlace por primera vez. ¡Después será rápido!

---

## 📸 Demostración del Sistema

### 1. Panel de Orquestación
*Monitoreo de riesgos en tiempo real con controladores de IA Explicable (SHAP).*
![Dashboard View](/images/dashboard_overview.png)
![Dashboard View](/images/dashboard_overview_2.png)


### 2. Despliegue Logístico en Vivo (Leaflet.js)
*Enrutamiento automatizado de ambulancias activado cuando el riesgo > 60%.*
![Live Map Simulation](/images/live_map_dispatch.png)


---

## 🚀 Características Principales

### 🧠 1. Detección de Anomalías con Conciencia de Contexto
En lugar de umbrales estáticos, HeaSphere analiza **Variables de Velocidad** (por ejemplo, qué tan rápido cambia el IMC en 2 años) utilizando un **Regresor XGBoost**. Esto nos permite captar "señales débiles" antes de que se conviertan en emergencias.

### 🔍 2. IA Explicable (XAI)
No confiamos en las "Cajas Negras". El sistema utiliza **SHAP (SHapley Additive exPlanations)** para generar un gráfico de barras dinámico para cada predicción, mostrando exactamente *por qué* la IA marcó un riesgo (por ejemplo, "La edad contribuyó +15%, pero el historial de presión arterial contribuyó +40%").

### 🚑 3. Despliegue Logístico Autónomo
Motor de **Triage Geoespacial** integrado:
- **Riesgo Bajo:** El sistema permanece en modo de "Monitoreo Pasivo".
- **Riesgo Alto (>60%):** Activa instantáneamente la capa logística de **Leaflet.js**, animando una simulación de despliegue de ambulancia en vivo desde la instalación "Hea-Certificada" más cercana a la ubicación geolocalizada del paciente.

### 🛡️ 4. "Gap de Aire" de Seguridad y Ética
- **No Diagnóstico:** La IA nunca realiza diagnósticos. Marca anomalías y transfiere el caso al **Asistente Hea**, que utiliza preguntas empáticas y no clínicas para recopilar contexto para un especialista humano.
- **Auditoría de Equidad:** El modelo se audita para garantizar la paridad de género (distribución de riesgo 39% Masculino / 33% Femenino) y prevenir sesgos algorítmicos.

---

## 🛠️ Stack Tecnológico

| Dominio | Tecnología | Caso de Uso |
| :--- | :--- | :--- |
| **Backend Central** | **Django 5.0 (Python)** | Arquitectura MVT, Endpoints de API, Lógica de Orquestación |
| **Motor de ML** | **XGBoost & CatBoost** | Modelo de Regresión de Anomalías (PR-AUC 0.85) |
| **Explicabilidad** | **SHAP** | Visualización de Importancia de Características |
| **Frontend** | **JavaScript & Tailwind** | Panel Asincrónico, Medidores Dinámicos |
| **Geoespacial** | **Leaflet.js & OpenStreetMap** | Mapas Interactivos, Animación de Rutas |
| **DevOps** | **Docker & GitHub Actions** | Contenedores, Pruebas Automatizadas CI/CD |
| **Despliegue** | **Render Cloud** | Hospedaje de Producción con Gunicorn/WhiteNoise |

---

## ⚙️ Instalación y Configuración Local

¿Desea ejecutar el Motor de Orquestación localmente?

**1. Clonar el Repositorio**
```bash
git clone [https://github.com/AdMub/hea-health-signals.git](https://github.com/AdMub/hea-health-signals.git)
cd hea-health-signals
```

### **2. Crear Entorno Virtual**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### **4. Ejecutar Migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```
### **5. Iniciar el Sistema**
```bash
python manage.py runserver
Access the dashboard at http://127.0.0.1:8000/.
```


### **🧪 Probar la Simulación**
Para ver el **Protocolo de Despliegue de Emergencia** en acción sin esperar la degradación de datos de salud reales:

1. Abra el Panel.
2. Haga clic en el enlace "Ejecutar Escenario de Demo" en el pie de página (o ingrese manualmente IMC: 35, Salud: 5, PA: Alta).
3. Observe cómo el Medidor de Riesgo se pone en rojo y la Ambulancia navega físicamente en el mapa hacia la zona objetivo.

📜 Licencia y Créditos
Autor: [Su Nombre]

Licencia: Licencia MIT

Contexto: Desarrollado para el Hea Health Hackathon (Enfoque: Señales de Salud con Conciencia de Contexto).

### **👨‍💻 Autor**

**Mubarak Adisa** *Ingeniero de IA y Desarrollador Full-Stack*

- 🎓 **Antecedentes:** Egresado de Ingeniería Civil en transición a Ciencias de la Computación, con un enfoque en Ciencia de Datos y Sistemas de IA.
- 🛠️ **Especialización:** Construcción de sistemas orquestados que conectan la infraestructura física (Logística/Civil) con la inteligencia digital (IA/ML).
- 🔗 **GitHub:** [AdMub](https://github.com/AdMub)  
- 💼 **LinkedIn:** [Mubarak Adisa](https://www.linkedin.com/in/mubarak-adisa-334a441b6/)

---

### **📄 Licencia**

Distribuido bajo la **Licencia MIT**. Consulte `LICENSE` para más información.  
*(Este proyecto es de código abierto con fines educativos y de portafolio.)*

---

### **🌟 Reconocimientos y Créditos**

HeaSphere se construyó como un prototipo de alta fidelidad para demostrar la **Orquestación de Salud con Conciencia de Contexto**.

- **Inspiración:** Desarrollado con la filosofía del **Hea Health Hackathon** (Detectar "Señales Débiles" antes de que se conviertan en emergencias).
- **Motor Geoespacial:** Impulsado por **Leaflet.js** y los contribuyentes de **OpenStreetMap** para la simulación de despacho en vivo.
- **Aprendizaje Automático:** Construido sobre los hombros de **XGBoost** y **SHAP** (slundberg/shap) para la explicabilidad del modelo.
- **Infraestructura:** Desplegado en **Render** Cloud; Backend impulsado por **Django Framework**.
