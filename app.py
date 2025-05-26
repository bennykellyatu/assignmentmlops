from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load the trained model
model_path = os.path.join('ModelCleaning', 'TemperatureProfitsModel.pkl')
try:
    model = joblib.load(model_path)
    print(f"Model loaded successfully from {model_path}")
except FileNotFoundError:
    print(f"Model file not found at {model_path}")
    model = None

@app.route('/')
def home():
    return jsonify({
        "message": "Ice Cream Profits Prediction API",
        "description": "Predict ice cream profits based on temperature",
        "endpoints": {
            "/predict": "POST - Make a prediction",
            "/health": "GET - Check API health"
        }
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    try:
        # Get temperature from request
        data = request.get_json()
        
        if 'temperature' not in data:
            return jsonify({"error": "Temperature value required"}), 400
        
        temperature = float(data['temperature'])
        
        # Make prediction
        temperature_array = np.array([[temperature]])
        prediction = model.predict(temperature_array)
        
        return jsonify({
            "temperature": temperature,
            "predicted_profit": round(float(prediction[0]), 2)
        })
    
    except ValueError:
        return jsonify({"error": "Invalid temperature value"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 