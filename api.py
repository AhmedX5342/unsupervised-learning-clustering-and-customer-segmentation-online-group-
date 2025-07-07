from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load model and scaler
kmeans = joblib.load('kmeans_model.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Prepare input data
        df = pd.DataFrame([data])
        df = df[['Total', 'Frequency', 'Quantity', 'UnitPrice']]  # Ensure column order

        # Scale and predict
        scaled = scaler.transform(df)
        cluster = kmeans.predict(scaled)

        return jsonify({'cluster': int(cluster[0])})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
