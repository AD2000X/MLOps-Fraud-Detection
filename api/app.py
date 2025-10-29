from flask import Flask, request, jsonify, render_template
import mlflow
import joblib # REVISED 29OCT25
import pandas as pd
import os
import logging
from mlflow.pyfunc import load_model
from flask_basicauth import BasicAuth
# Monitoring
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from flask import Flask, request, jsonify, render_template, Response
import time

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('AUTH_USERNAME', 'admin')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('AUTH_PASSWORD', 'password')

basic_auth = BasicAuth(app)
# Monitoring
# ==========================================
# Prometheus Metrics
# ==========================================
# Counter: Total number of predictions
prediction_counter = Counter(
    'fraud_predictions_total',
    'Total number of fraud predictions',
    ['prediction_result']  # Label: fraud or not_fraud
)

# Histogram: Prediction latency
prediction_latency = Histogram(
    'fraud_prediction_latency_seconds',
    'Time taken for fraud prediction',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0]  # Delay interval
)

# Gauge: Model accuracy (needs periodic updates)
model_accuracy = Gauge(
    'fraud_model_accuracy',
    'Current accuracy of the fraud detection model'
)

# Gauge: Confidence score of the most recent prediction
prediction_confidence = Gauge(
    'fraud_prediction_confidence',
    'Confidence score of the last prediction'
)

# Initialize accuracy (from training results)
model_accuracy.set(0.9996)  # 99.96% from our training results



# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Environment variables and default values
# MODEL_URI = os.getenv('MODEL_URI', 'models:/fraud_detection/Production')
# SERVER_PORT = os.getenv('PORT', '8000')
# DEBUG_MODE = os.getenv('DEBUG', 'False').lower() == 'true'

# # Load the model
# try:
#     model = load_model(MODEL_URI)
#     logging.info("Model loaded successfully.")
# except Exception as e:
#     logging.error(f"Error loading model: {e}")
#     model = None

# REVISED 29OCT25
MODEL_PATH = os.getenv('MODEL_PATH', 'model/saved_models/model.pkl')
SERVER_PORT = os.getenv('PORT', '8000')
DEBUG_MODE = os.getenv('DEBUG', 'False').lower() == 'true'

# Load the model
try:
    model = joblib.load(MODEL_PATH)
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    model = None
# REVISED 29OCT25

@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@basic_auth.required
def predict():
    """Endpoint to make fraud detection predictions."""
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    data = request.form.to_dict()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Start timing
    start_time = time.time()

    try:
        # Input validation
        required_fields = [
            'Time', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9',
            'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18',
            'V19', 'V20', 'V21', 'V22', 'V23', 'V24', 'V25', 'V26', 'V27',
            'V28', 'Amount'
        ]

        if not all(field in data for field in required_fields):
            return jsonify({'error':
                            'Missing required fields in input data'}), 400

        df = pd.DataFrame([data])
        prediction = model.predict(df)[0]  # Probability of class 1 (fraud)
        logging.info(f"Prediction: {prediction}")
        is_fraud = prediction > 0.5

        # Record delay
        latency = time.time() - start_time
        prediction_latency.observe(latency)

        # Record prediction results
        result_label = 'fraud' if is_fraud else 'not_fraud'
        prediction_counter.labels(prediction_result=result_label).inc()

        # Record confidence score
        confidence = float(prediction) if is_fraud else float(1 - prediction)
        prediction_confidence.set(confidence)

        # Log prediction and input data for monitoring
        logging.info(f"Prediction: {prediction}, Is Fraud: {is_fraud}, Latency: {latency:.4f}s")

        return jsonify({
            'prediction': float(prediction),
            'is_fraud': bool(is_fraud),
            'confidence': confidence,
            'latency_seconds': latency
        })

    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return jsonify({'error': 'An error occurred during prediction'}), 500

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), mimetype='text/plain')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(SERVER_PORT), debug=DEBUG_MODE)
