# LogLens 🛡️

LogLens (also referred to as LOG GUARD) is an advanced log analysis and security monitoring platform designed to provide a smart layer of defense for your NGINX logs, helping you detect and prevent threats before they spread.

---

## 🔥 Live Demo (Watch First!)

[![Watch the demo](https://img.youtube.com/vi/7SMugMNYbok/0.jpg)](https://youtu.be/7SMugMNYbok)

> 👆 Watch how LogLens monitors, detects, and visualizes real-time threats in seconds!

---

## 🚀 Features

- **Real-time Monitoring:** Monitor logs in real time with advanced analytics and threat detection algorithms. ⏱️
- **AI-Powered Analysis:** Leverage machine learning model (CatBoost) to automatically identify patterns and potential security threats. 🤖
- **Automated Alerts:** Receive instant notifications when suspicious activities are detected in your logs. 🚨
- **Comprehensive Reports:** Generate detailed security reports and analytics for compliance and auditing. 📊
- **Interactive Dashboard:** Visualize system health, recent anomalies, and traffic patterns. 💻
- **AI Chat Assistant:** Chat-based interface for log analysis help and quick anomaly queries. 💬

---

## 📊 Model Performance

LogLens utilizes machine learning algorithms for anomaly detection with the following performance metrics (evaluated on test data):

- **Recall:** 95%
- **Precision:** 100%
- **F1-score:** 97%

> These results indicate that LogLens can accurately detect almost all true threats (high recall) with no false positives (perfect precision), ensuring robust and reliable security monitoring. ✅

---

## 🏗️ Architecture Overview

LogLens consists of several main components:

- **Web Frontend:** Built using HTML, CSS, and JavaScript, providing an interactive dashboard and chat assistant.
- **Backend/API:** Implemented in Python (Flask), serving data, managing user authentication, and running analysis models. 🐍
- **AI/ML Analysis:** Uses Python and Jupyter Notebook for machine learning-based anomaly detection. 🧠
- **Standalone & Integrated Modes:** UI can run in standalone HTML mode or as part of a Flask web app.
- **Chatbot:** Integrated chatbot interface for conversational log analysis.

---

## 📁 Main Directories

- `web/`: HTML, CSS, and JS files for the dashboard and standalone demo.
- `LogLensApp/`: Flask app templates and backend logic.
- `Chatbot/`: Chatbot interface and backend.
- `notebooks/`: Jupyter Notebooks for AI/ML modeling.

---

## ⚙️ How It Works

1. **Data Ingestion:** LogLens ingests NGINX logs and other security logs. 📥  
2. **Analysis:** ML algorithms detect anomalies and threats in near real time.  
3. **Visualization:** Interactive dashboard displays system health and anomalies. 📈  
4. **Alerts & Chat:** Instant alerts and chat-based log analysis support.

---

## 🧰 Installation & Getting Started

### ✅ Prerequisites

- Python 3.7+
- Node.js (for chatbot or extra JS features)
- (Optional) Jupyter Notebook

### 📦 Clone the Repository

```bash
git clone https://github.com/pexa8335/LogLens.git
cd LogLens
```

### 🖥️ Backend Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Start backend services:

```bash
python app.py
python worker.py
python normal_traffic_generator.py
python anomaly_traffic_generator.py
```
>🔧 You can customize worker.py to point to your actual LOG_FILE_PATH.

### 🌐 Frontend Setup
- Standalone mode:
Open `web/standalone.html` directly in your browser for a quick demo.

- Full web app mode:
After starting the Flask backend, visit:

```arduino
http://localhost:5000
```

### 💬 Chatbot Usage
- Access the chatbot via the dashboard UI.

- Or run it independently from the Chatbot/ directory.

### 🧪 Customization
- Log Sources: Configure via backend or dashboard settings.

- ML Models: Retrain or modify logic in the notebooks/ or Python scripts.

### 🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request. 🙏

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).

You are free to use, modify, and distribute this software for personal or commercial purposes, provided that the original license and copyright
notice are retained.

---
>LogLens — A smart, AI-powered platform for log security, anomaly detection, and compliance. ✨