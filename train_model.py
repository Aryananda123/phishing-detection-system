import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from feature_extraction import extract_features, get_feature_names

def train():
    print("Loading dataset...")
    # Load dataset
    data_path = os.path.join('data', 'sample_dataset.csv')
    if not os.path.exists(data_path):
        alt_path = os.path.join('data', 'sample_dataset (1).csv')
        if os.path.exists(alt_path):
            data_path = alt_path
            print(f"Using dataset file '{os.path.basename(data_path)}'")
        else:
            print(f"Error: Dataset not found at {data_path}")
            return

    df = pd.read_csv(data_path)
    
    print("Extracting features...")
    # Extract features for all URLs
    features_list = []
    for url in df['url']:
        features = extract_features(url)
        features_list.append(list(features.values()))
        
    X = np.array(features_list)
    y = df['label'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    os.makedirs('models', exist_ok=True)
    model_path = os.path.join('models', 'rf_model.pkl')
    joblib.dump(model, model_path)
    print(f"Model saved successfully to {model_path}")

if __name__ == "__main__":
    train()
