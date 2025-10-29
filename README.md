# Fraud Detection Application

This repository contains a machine learning application for fraud detection. It uses a RandomForest classifier to predict fraudulent activities and is built with Flask, deployed using Docker, and orchestrated with GitHub Actions for CI/CD. MLflow is used for model tracking and management.

## Key Features
- Automated detection of potential fraud in financial transactions.
- Regular retraining capabilities to adapt to data drift.
- RESTful API for accessing model predictions.
- MLflow integration for model performance monitoring.
- Automated workflow using GitHub Actions for model retraining and deployment.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8 or higher
- Docker installed
- Access to a terminal/command line interface
- GitHub account (for CI/CD using GitHub Actions)
- Azure account (if deploying to Azure Web App)

## Installation

To install the Fraud Detection Application, follow these steps:

1. Clone the repository:
   ```
   git clone [repository-url]
   ```

2. Navigate to the cloned directory:
   ```
   cd [local-repository]
   ```

3. (Optional) Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. Install required packages:
   ```
   pip install -r requirements.txt
   ```


## Training and Evaluating the Model and 

To train the model, run:

```
python /model/model.py
```

This will load the test data and the trained model, then output evaluation metrics.

## Running the Application Locally

To run the application locally:

1. Start the Flask app:
   ```
   python /api/app.py
   ```

2. The application will be available at `http://127.0.0.1:8000/`.


## Running the Application
1. **Train the model**:
   ```
   python model/model.py
   ```
2. **Start the Flask API**:
   ```
   python api/app.py
   ```
3. **Send prediction requests** (using tools like `curl` or Postman):
   ```
   curl -X POST -H "Content-Type: application/json" -d '{"Time": ..., "V1": ..., ...}' http://127.0.0.1:8000/predict
   ```
   - Sample request is like:
   ```
   curl -X POST -H "Content-Type: application/json" -d '{"Time": 119907, "V1": -0.611712, "V2": -0.769705, "V3": -0.149759, "V4": -0.224877, "V5": 2.028577, "V6": -2.019887, "V7": 0.292491, "V8": -0.523020, "V9": 0.358468, "V10": -0.507582, "V11": -1.205419, "V12": 0.564061, "V13": -0.190509, "V14": 0.191617, "V15": 0.301595, "V16": -0.408111, "V17": 0.299503, "V18": -0.209950, "V19": 0.770147, "V20": 0.202402, "V21": -0.075208, "V22": 0.045536, "V23": 0.380739, "V24": 0.023440, "V25": -2.220686, "V26": -0.201146, "V27": 0.066501, "V28": 0.221180, "Amount": 1.79}' http://127.0.0.1:8000/predict
   ```


## Deploying with Docker

To deploy the application using Docker:

1. Build the Docker image:
   ```
   docker build -t fraud-detector .
   ```

2. Run the Docker container:
   ```
   docker run -p 8000:8080 fraud-detector
   ```

The application will be available at `http://localhost:8080`.

## CI/CD with GitHub Actions

The `.github/workflows/ml-ops-workflow.yml` file defines the GitHub Actions workflow for continuous integration and deployment. Pushing changes to the main branch will trigger the workflow. Also the workflow is triggered every month to retrain the model.

## Using MLflow for Model Tracking

To track models using MLflow, ensure MLflow server is running and accessible. The training and evaluation scripts are set up to log metrics and parameters to MLflow. 
```
mlflow ui
```


## Monitoring

This project uses Prometheus and Grafana for real-time monitoring.

### 📊 Grafana Dashboard

![Grafana Dashboard](docs/images/grafana-dashboard.jpg)

The complete monitoring dashboard includes:

- **Total Predictions**: 167 predictions

- **Fraud vs Normal**: Fraud 38% vs Normal 62%

- **Model Accuracy**: 99.96% accuracy

- **Average Latency**: 13.5ms response time

- **Predictions Over Time**: Real-time trend chart

### 🎯 Prometheus Monitoring

#### Targets Status

![Prometheus Targets](docs/images/prometheus-targets.jpg)

Prometheus successfully monitored the following services:

- ✅ `fraud-detection-api` - UP (http://fraud-detector:8000/metrics)

- ✅ `prometheus` - UP (http://localhost:9090/metrics)

#### Query Examples

**Fraud Predictions:**

![Fraud Predictions](docs/images/prometheus-query-fraud.jpg)

**Normal Predictions:**

![Normal Predictions](docs/images/prometheus-query-normal.jpg)

**Service Discovery:**

![Service Discovery](docs/images/prometheus-service-discovery.jpg)

### Monitoring Metrics

| Metric | Description | Current Value | Query |

|------|------|--------|---------|

| **Total Predictions** | Total Predictions | 167 | `sum(fraud_predictions_total)` |

| **Fraud Rate** | Fraud Detection Rate | 38% | `fraud_predictions_total{prediction_result="fraud"}` |

| **Model Accuracy** | Model accuracy | 99.96% | `fraud_model_accuracy` |

| **Avg Latency** | Average response time | 13.5ms | `fraud_prediction_latency_seconds_sum / fraud_prediction_latency_seconds_count` |

### Start the monitoring system

```bash
cd monitoring
docker-compose up -d

```

### Access the monitoring panel

- **Grafana Dashboard**: http://localhost:3000

- Username: `admin`

- Password: `admin`

- **Prometheus UI**: http://localhost:9090

- **API Metrics**: http://localhost:8000/metrics

### Commonly used PromQL queries

```promql

# Prediction rate per minute

rate(fraud_predictions_total[1m]) * 60

# Fraud detections in the past hour

increase(fraud_predictions_total{prediction_result="fraud"}[1h])

# Fraud rate

fraud_predictions_total{prediction_result="fraud"} / sum(fraud_predictions_total) * 100

# P95 latency

histogram_quantile(0.95, rate(fraud_prediction_latency_seconds_bucket[5m]))

```

### Stop monitoring

```bash
docker-compose down
```


## License
This project is licensed under the terms of the MIT License

## Contact
- Please feel free to contact me if you have any questions or suggestions
- Mohammadsadegh Solouki - mohamad.solouki@gmail.com
