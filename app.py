from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import os
from feature_extraction import extract_features

app = Flask(__name__)

# Load the trained model
MODEL_PATH = os.path.join('models', 'rf_model.pkl')
try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded. Please train the model first.'}), 500
        
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided.'}), 400
        
    url = data['url']
    
    try:
        # Extract features
        features = extract_features(url)
        features_array = np.array([list(features.values())])

        if hasattr(model, 'n_features_in_') and features_array.shape[1] != model.n_features_in_:
            return jsonify({
                'error': f'Model expects {model.n_features_in_} features, but extractor produced {features_array.shape[1]}. Please retrain the model with the current feature extractor.'
            }), 500

        # Predict
        prediction = model.predict(features_array)[0]
        probability = model.predict_proba(features_array)[0]

        result = {
            'url': url,
            'is_phishing': bool(prediction == 1),
            'risk_score': float(probability[1] * 100), # Percentage
            'features_analyzed': features
        }
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
