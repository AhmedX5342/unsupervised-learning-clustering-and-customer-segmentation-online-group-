# from flask import Flask, request, jsonify
# import joblib
# import pandas as pd

# app = Flask(__name__)

# # Load model and scaler
# kmeans = joblib.load('kmeans_model.pkl')
# scaler = joblib.load('scaler.pkl')

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         data = request.get_json()

#         # Prepare input data
#         df = pd.DataFrame([data])
#         df = df[['Total', 'Frequency', 'Quantity', 'UnitPrice']]  # Ensure column order

#         # Scale and predict
#         scaled = scaler.transform(df)
#         cluster = kmeans.predict(scaled)

#         return jsonify({'cluster': int(cluster[0])})
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load the model and scaler
model = joblib.load('kmeans_model.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Read uploaded Excel file
        file = request.files['file']
        df = pd.read_excel(file)

        # Match preprocessing from training script
        features = df[['InvoiceNo', 'Quantity', 'UnitPrice', 'Country']].copy()
        features[['Quantity', 'UnitPrice']] = features[['Quantity', 'UnitPrice']].apply(pd.to_numeric, errors='coerce')
        features['InvoiceNo'] = pd.to_numeric(features['InvoiceNo'], errors='coerce')
        features.dropna(subset=['InvoiceNo', 'Quantity', 'UnitPrice', 'Country'], inplace=True)
        features = features[(features['Quantity'] > 0) & (features['UnitPrice'] > 0)]
        features['InvoiceNo'] = features['InvoiceNo'].astype(int)
        features['Total'] = features['Quantity'] * features['UnitPrice']
        invoice_freq = features['InvoiceNo'].value_counts()
        features['Frequency'] = features['InvoiceNo'].map(invoice_freq)

        # Extract input for prediction
        X = features[['Total', 'Frequency', 'Quantity', 'UnitPrice']]
        X_scaled = scaler.transform(X)

        # Predict clusters
        cluster_preds = model.predict(X_scaled)
        features['Cluster'] = cluster_preds

        # Optional labels
        cluster_labels = {
            0: "High-Value Repeat Buyers",
            1: "One-Time Medium Buyers",
            2: "Low-Value Occasional Buyers",
            3: "Frequent Low-Spenders"
        }
        features['Cluster_Label'] = features['Cluster'].map(cluster_labels)

        # Return result
        return jsonify(features[['InvoiceNo', 'Quantity', 'UnitPrice', 'Total', 'Frequency', 'Cluster', 'Cluster_Label']].head(50).to_dict(orient='records'))

    except Exception as e:
        return jsonify({'error': 'Model prediction failed', 'details': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
