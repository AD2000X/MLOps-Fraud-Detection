# MLOps Fraud Detection System

[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.0-orange.svg)](https://scikit-learn.org/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)
[![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-red.svg)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/Grafana-Dashboard-orange.svg)](https://grafana.com/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-green.svg)](https://github.com/features/actions)

> A complete MLOps credit card fraud detection system featuring model training, API deployment, CI/CD automation, and real-time monitoring.

![Grafana Dashboard](docs/images/grafana.jpg)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Monitoring System](#monitoring-system)
- [CI/CD Pipeline](#cicd-pipeline)
- [API Documentation](#api-documentation)
- [Development Guide](#development-guide)
- [Project Results](#project-results)

---

## Project Overview

This project demonstrates a complete MLOps workflow including:

- **Machine Learning Model**: Random Forest credit card fraud detection model
- **RESTful API**: Flask-based prediction service with Basic Authentication
- **Containerization**: Fully Dockerized for one-click deployment
- **Real-time Monitoring**: Prometheus + Grafana monitoring system
- **CI/CD Automation**: GitHub Actions automated testing and deployment
- **Large File Management**: Git LFS for training data and models

### Project Highlights

- **Model Accuracy**: 99.96%
- **API Latency**: Average 13.5ms
- **Successful Predictions**: 167+
- **Fraud Detection Rate**: 38%

---

## Key Features

- **Automated Fraud Detection**: Real-time detection of fraudulent financial transactions
- **RESTful API**: Easy-to-integrate prediction endpoint with authentication
- **Model Performance Monitoring**: Track accuracy, latency, and prediction trends
- **Intelligent CI/CD**: Separate pipelines for code changes vs documentation updates
- **Production Ready**: Docker containerization with health checks and metrics
- **Real-time Dashboards**: Beautiful Grafana visualizations of system metrics

---

## Technology Stack

### **Machine Learning**
- Python 3.9
- scikit-learn 1.3.0
- pandas 2.0.3
- numpy 1.24.3
- Random Forest Classifier

### **Web Framework**
- Flask 2.3.3
- Flask-BasicAuth 0.2.0

### **Containerization**
- Docker
- Docker Compose

### **Monitoring**
- Prometheus
- Grafana
- prometheus-client

### **CI/CD**
- GitHub Actions
- Git LFS

---

## Project Structure
```
MLOps-Fraud-Detection/
├── .github/
│   └── workflows/
│       ├── ml-pipeline.yml          # Code CI/CD Pipeline
│       └── docs-check.yml           # Documentation Workflow
├── api/
│   ├── app.py                       # Flask API with Prometheus metrics
│   ├── Dockerfile                   # API container configuration
│   └── templates/
│       └── index.html               # Web interface
├── model/
│   └── saved_models/
│       └── model.pkl                # Trained model (157MB, Git LFS)
├── data/
│   └── creditcard.csv               # Training dataset (150MB, Git LFS)
├── monitoring/
│   ├── docker-compose.yml           # Full system orchestration
│   ├── prometheus/
│   │   └── prometheus.yml           # Prometheus configuration
│   └── grafana/
│       └── datasources/
│           └── prometheus.yml       # Grafana datasource
├── docs/
│   └── images/                      # Monitoring screenshots
├── .gitattributes                   # Git LFS configuration
├── .gitignore
├── requirements.txt                 # Python dependencies (pinned versions)
└── README.md
```

---

## Quick Start

### **Prerequisites**

- Docker & Docker Compose
- Python 3.9+
- Git LFS

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/AD2000X/MLOps-Fraud-Detection.git
cd MLOps-Fraud-Detection

# Pull LFS files
git lfs pull
```

### **Step 2: Launch the Complete System**
```bash
cd monitoring
docker-compose up -d
```

### **Step 3: Access Services**

| Service | URL | Credentials |
|---------|-----|-------------|
| **API Interface** | http://localhost:8000 | admin / password |
| **Prometheus** | http://localhost:9090 | - |
| **Grafana** | http://localhost:3000 | admin / admin |

### **Step 4: Test Predictions**

**Using cURL:**
```bash
curl -u admin:password -X POST http://localhost:8000/predict \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "Time=406&V1=-2.312226&V2=1.951992&V3=-1.609851&V4=3.997906&V5=-0.522188&V6=-1.426545&V7=-2.537387&V8=1.391657&V9=-2.770089&V10=-2.772272&V11=3.202033&V12=-2.899907&V13=-0.595222&V14=-4.289254&V15=0.389724&V16=-1.140747&V17=-2.830056&V18=-0.016822&V19=0.416956&V20=0.126911&V21=0.517232&V22=-0.035049&V23=-0.465211&V24=0.320198&V25=0.044519&V26=0.177840&V27=0.261145&V28=-0.143276&Amount=0.0"
```

**Using PowerShell:**
```powershell
$headers = @{
    Authorization = "Basic " + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:password"))
}

$body = "Time=406&V1=-2.312226&V2=1.951992&..."

Invoke-RestMethod -Uri "http://localhost:8000/predict" `
    -Method POST -Headers $headers -Body $body `
    -ContentType "application/x-www-form-urlencoded"
```

**Expected Response:**
```json
{
  "prediction": 0.9876,
  "is_fraud": true,
  "confidence": 0.9876,
  "latency_seconds": 0.0135
}
```

---

## Monitoring System

### **Grafana Dashboard**

![Grafana Dashboard](docs/images/grafana-dashboard.jpg)

The complete monitoring dashboard includes 5 key panels:

1. **Total Predictions** - Total number of predictions made
2. **Fraud vs Normal** - Fraud and normal transaction distribution
3. **Model Accuracy** - Model accuracy gauge (target >99.5%)
4. **Average Latency** - Average response time
5. **Predictions Over Time** - Real-time prediction trends

### **Prometheus Targets**

![Prometheus Targets](docs/images/prometheus-targets.jpg)

Prometheus successfully monitors the following services:
- **fraud-detection-api** - UP (http://fraud-detector:8000/metrics)
- **prometheus** - UP (http://localhost:9090/metrics)

### **Monitoring Metrics**

| Metric | Description | Current Value | PromQL Query |
|--------|-------------|---------------|--------------|
| **Total Predictions** | Total predictions made | 167 | `sum(fraud_predictions_total)` |
| **Fraud Rate** | Fraud detection rate | 38% | `fraud_predictions_total{prediction_result="fraud"}` |
| **Model Accuracy** | Model accuracy | 99.96% | `fraud_model_accuracy` |
| **Avg Latency** | Average response time | 13.5ms | `fraud_prediction_latency_seconds_sum / fraud_prediction_latency_seconds_count * 1000` |

### **Prometheus Query Examples**

![Fraud Predictions](docs/images/prometheus-query-fraud.jpg)
![Normal Predictions](docs/images/prometheus-query-normal.jpg)

**Fraud transaction trends:**
```promql
fraud_predictions_total{prediction_result="fraud"}
```

**Normal transaction trends:**
```promql
fraud_predictions_total{prediction_result="not_fraud"}
```

**Prediction rate per minute:**
```promql
rate(fraud_predictions_total[1m]) * 60
```

**Fraud ratio:**
```promql
fraud_predictions_total{prediction_result="fraud"} / sum(fraud_predictions_total) * 100
```

**P95 latency:**
```promql
histogram_quantile(0.95, rate(fraud_prediction_latency_seconds_bucket[5m]))
```

---

## CI/CD Pipeline

### **Intelligent Dual Pipeline Architecture**

The project uses two independent GitHub Actions workflows:

#### **1. ML Pipeline** (`.github/workflows/ml-pipeline.yml`)

**Trigger Conditions:** Code or model changes
```yaml
paths:
  - 'api/**'
  - 'model/**'
  - 'requirements.txt'
  - 'Dockerfile'
```

**Execution Stages:**
1. **Code Quality Check** - Python syntax validation (~45s)
2. **Validate Model** - Model validation (~5s)
3. **Build and Test Docker** - Container build and testing (~3-4min)
4. **Pipeline Summary** - Execution report (~5s)

**Total execution time:** ~4-5 minutes

#### **2. Documentation Check** (`.github/workflows/docs-check.yml`)

**Trigger Conditions:** Documentation or image changes
```yaml
paths:
  - 'docs/**'
  - '*.md'
  - '**/*.jpg'
  - '**/*.png'
```

**Execution Stages:**
1. **Check Documentation** - Validate documentation (~30s)
2. **Documentation Report** - Statistics report (~5s)

**Total execution time:** ~30 seconds

### **CI/CD Optimization Results**

| Change Type | Before | After | Savings |
|-------------|--------|-------|---------|
| Update README | 7 min | 30s | 93%  |
| Add images | 7 min | 30s | 93%  |
| Modify API | 7 min | 5 min | 29%  |

---

## API Documentation

### **Endpoints**

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/` | GET | Web prediction interface |
| `/predict` | POST | Prediction endpoint |
| `/health` | GET | Health check |
| `/metrics` | GET | Prometheus metrics |

### **POST /predict**

**Request Format:**
```
Content-Type: application/x-www-form-urlencoded
Authorization: Basic YWRtaW46cGFzc3dvcmQ=
```

**Request Parameters:**
- `Time`: Transaction time (seconds)
- `V1-V28`: PCA-transformed features
- `Amount`: Transaction amount

**Response Format:**
```json
{
  "prediction": 0.9876,
  "is_fraud": true,
  "confidence": 0.9876,
  "latency_seconds": 0.0135
}
```

### **GET /health**

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### **GET /metrics**

**Prometheus format metrics:**
```
# HELP fraud_predictions_total Total number of fraud predictions
# TYPE fraud_predictions_total counter
fraud_predictions_total{prediction_result="fraud"} 64.0
fraud_predictions_total{prediction_result="not_fraud"} 103.0

# HELP fraud_model_accuracy Current accuracy of the fraud detection model
# TYPE fraud_model_accuracy gauge
fraud_model_accuracy 0.9996

# HELP fraud_prediction_latency_seconds Time taken for fraud prediction
# TYPE fraud_prediction_latency_seconds histogram
fraud_prediction_latency_seconds_bucket{le="0.01"} 150.0
fraud_prediction_latency_seconds_sum 2.25
fraud_prediction_latency_seconds_count 167.0
```

---

## Development Guide

### **Local Development Setup**
```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run API
python api/app.py

# 4. Access
# http://localhost:8000
```

### **Docker Development**
```bash
# Build image
docker build -t fraud-detector .

# Run container
docker run -p 8000:8000 \
  -e AUTH_USERNAME=admin \
  -e AUTH_PASSWORD=password \
  fraud-detector
```

### **Monitoring System Development**
```bash
# Start full system
cd monitoring
docker-compose up -d

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart grafana

# Stop system
docker-compose down
```

### **Useful Commands**
```bash
# Git LFS
git lfs install
git lfs track "*.pkl"
git lfs ls-files
git lfs pull

# Docker
docker ps
docker logs 
docker-compose ps
docker-compose logs -f

# Testing
curl http://localhost:8000/health
curl http://localhost:8000/metrics
```

---

## Project Results

### **Model Performance**
- **Accuracy**: 99.96%
- **Training Data**: 284,807 transaction records
- **Features**: 30 (Time, V1-V28, Amount)
- **Algorithm**: Random Forest Classifier

### **API Performance**
- **Average Latency**: 13.5ms
- **Successful Predictions**: 167+
- **Fraud Detection**: 38% rate
- **Normal Transactions**: 62% rate

### **DevOps Metrics**
- **CI/CD Execution Time**: 4-5 minutes (code changes)
- **Documentation Check**: 30 seconds
- **Docker Build**: 3-4 minutes
- **Automation Coverage**: 100%

---

## Learning Resources

- [scikit-learn Documentation](https://scikit-learn.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## Acknowledgments

- Kaggle for the credit card fraud dataset
- scikit-learn team
- Flask, Prometheus, Grafana open-source communities

---
