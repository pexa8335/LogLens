# LogLens

  

LogLens (also referred to as LOG GUARD) is an advanced log analysis and security monitoring platform designed to provide a smart layer of defense for your NGINX logs, helping you detect and prevent threats before they spread.

  

## Features

  

- **Real-time Monitoring:** Monitor logs in real time with advanced analytics and threat detection algorithms.

- **AI-Powered Analysis:** Leverage machine learning model (CatBoost) to automatically identify patterns and potential security threats.

- **Automated Alerts:** Receive instant notifications when suspicious activities are detected in your logs.

- **Comprehensive Reports:** Generate detailed security reports and analytics for compliance and auditing.

- **Interactive Dashboard:** Visualize system health, recent anomalies, and traffic patterns.

- **AI Chat Assistant:** Chat-based interface for log analysis help and quick anomaly queries.

  

## Model Performance

  

LogLens utilizes machine learning algorithms for anomaly detection with the following performance metrics (evaluated on test data):

  

- **Recall:** 95%

- **Precision:** 100%

- **F1-score:** 97%

  

These results indicate that LogLens can accurately detect almost all true threats (high recall) with no false positives (perfect precision), ensuring robust and reliable security monitoring.

  

## Architecture Overview

LogLens consists of several main components:

- **Web Frontend:** Built using HTML, CSS, and JavaScript, providing an interactive dashboard and chat assistant.

- **Backend/API:** Primarily implemented in Python, serving data, managing user authentication, and running analysis models.

- **AI/ML Analysis:** Utilizes Python and Jupyter Notebook for machine learning-based anomaly detection and pattern recognition.

- **Standalone & Integrated Modes:** The UI can run in standalone HTML mode or as part of a larger Flask web application.

- **Chatbot:** Integrates a chatbot interface for conversational log analysis.

## 🔥 Live Demo (Watch First!)

<video controls src="Screen Recording 2025-07-03 143853.mp4" title="LogLens Demo"></video>

> 👆 Watch how LogLens monitors, detects, and visualizes real-time threats in seconds!

### Main Directories

- `web/`: Contains HTML, CSS, and JavaScript files for the web dashboard and standalone demo.

- `LogLensApp/`: Flask app templates and backend logic.

- `Chatbot/`: Chatbot component and supporting files.

- Notebooks and scripts for AI/ML analysis.

## How It Works

1. **Data Ingestion:** LogLens ingests NGINX logs and other security logs.

2. **Analysis:** Logs are analyzed in near real time using ML algorithms for threat detection and anomaly spotting.

3. **Visualization:** Results are visualized on an interactive dashboard, showing system health, alerts, and recent anomalies.

4. **Alerts & Chat:** Users receive notifications and can interact with the AI Chat Assistant or Detect Anomaly Page for further insights, explanation or queries.


## Installation & Getting Started

### Prerequisites

- Python 3.7+

- Node.js (for chatbot or additional JS features, if needed)

- (Optional) Jupyter Notebook for running analysis notebooks

### Clone the Repository

```bash

git clone https://github.com/pexa8335/LogLens.git

cd LogLens

```

### Backend Setup

1. (Recommended) Create a virtual environment:

    ```bash

    python -m venv venv

    source venv/bin/activate  # On Windows: venv\Scripts\activate

    ```


2. Install dependencies:

    ```bash

    pip install -r requirements.txt

    ```

3. Start the Flask backend:

    ```bash

    python app.py

    python worker.py

    python normal_traffic_generator.py

    python anomaly_traffic_generator.py

    ```

You can customize the worker.py LOG_FILE_PATH to ensure it match your nginx web server.

### Frontend Setup 

- To run the standalone dashboard:

    - Open `web/standalone.html` directly in your browser for a demo.

- For the full web app:

    - Access `http://localhost:5000` after starting the Flask backend.

### Using the Chatbot

- The chatbot can be accessed via the dashboard interface or directly in the `Chatbot/` directory if running separately.

## Customization

- **Log Sources:** Configure your log sources in the backend or via the dashboard settings.

- **AI/ML Models:** Update or retrain models in the `notebooks/` and Python scripts for custom detection logic.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

See [LICENSE](LICENSE) for details.

---

**LogLens** — A smart, AI-powered platform for log security, anomaly detection, and compliance.# LogLens 🛡️

LogLens (also referred to as LOG GUARD) is an advanced log analysis and security monitoring platform designed to provide a smart layer of defense for your NGINX logs, helping you detect and prevent threats before they spread.

## Features

- **Real-time Monitoring:** Monitor logs in real time with advanced analytics and threat detection algorithms. ⏱️
- **AI-Powered Analysis:** Leverage machine learning model (CatBoost) to automatically identify patterns and potential security threats. 🤖
- **Automated Alerts:** Receive instant notifications when suspicious activities are detected in your logs. 🚨
- **Comprehensive Reports:** Generate detailed security reports and analytics for compliance and auditing. 📊
- **Interactive Dashboard:** Visualize system health, recent anomalies, and traffic patterns. 💻
- **AI Chat Assistant:** Chat-based interface for log analysis help and quick anomaly queries. 💬

## Model Performance

LogLens utilizes machine learning algorithms for anomaly detection with the following performance metrics (evaluated on test data):

- **Recall:** 95%
- **Precision:** 100%
- **F1-score:** 97%

These results indicate that LogLens can accurately detect almost all true threats (high recall) with no false positives (perfect precision), ensuring robust and reliable security monitoring. ✅

## Architecture Overview

LogLens consists of several main components:

- **Web Frontend:** Built using HTML, CSS, and JavaScript, providing an interactive dashboard and chat assistant.
- **Backend/API:** Primarily implemented in Python, serving data, managing user authentication, and running analysis models. 🐍
- **AI/ML Analysis:** Utilizes Python and Jupyter Notebook for machine learning-based anomaly detection and pattern recognition. 🧠
- **Standalone & Integrated Modes:** The UI can run in standalone HTML mode or as part of a larger Flask web application.
- **Chatbot:** Integrates a chatbot interface for conversational log analysis.

### Main Directories

- `web/`: Contains HTML, CSS, and JavaScript files for the web dashboard and standalone demo.
- `LogLensApp/`: Flask app templates and backend logic.
- `Chatbot/`: Chatbot component and supporting files.
- Notebooks and scripts for AI/ML analysis.

## How It Works

1. **Data Ingestion:** LogLens ingests NGINX logs and other security logs. 📥
2. **Analysis:** Logs are analyzed in near real time using ML algorithms for threat detection and anomaly spotting.
3. **Visualization:** Results are visualized on an interactive dashboard, showing system health, alerts, and recent anomalies. 📈
4. **Alerts & Chat:** Users receive notifications and can interact with the AI Chat Assistant or Detect Anomaly Page for further insights, explanation or queries.

## Installation & Getting Started

### Prerequisites

- Python 3.7+
- Node.js (for chatbot or additional JS features, if needed)
- (Optional) Jupyter Notebook for running analysis notebooks

### Clone the Repository

```bash
git clone https://github.com/pexa8335/LogLens.git
cd LogLens
```

### Backend Setup

1. (Recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the Flask backend:
   ```bash
   python app.py
   python worker.py
   python normal_traffic_generator.py
   python anomaly_traffic_generator.py
   ```

You can customize the worker.py LOG_FILE_PATH to ensure it match your nginx web server.

### Frontend Setup

- To run the standalone dashboard:
  - Open `web/standalone.html` directly in your browser for a demo.
- For the full web app:
  - Access `http://localhost:5000` after starting the Flask backend.

### Using the Chatbot

- The chatbot can be accessed via the dashboard interface or directly in the `Chatbot/` directory if running separately.

## Customization

- **Log Sources:** Configure your log sources in the backend or via the dashboard settings. ⚙️
- **AI/ML Models:** Update or retrain models in the `notebooks/` and Python scripts for custom detection logic.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request. 🙏

## License

See [LICENSE](LICENSE) for details.

---

**LogLens** — A smart, AI-powered platform for log security, anomaly detection, and compliance. ✨
