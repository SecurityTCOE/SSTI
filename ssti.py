from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from waitress import serve
from utils import custom_tokenizer  # Assuming custom_tokenizer is defined in utils.py

app = Flask(__name__)
CORS(app)  # Allow Cross-Origin Resource Sharing

# Load the best model
def load_model():
    try:
        return joblib.load('SSTI.pkl')
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

model = load_model()

if model is None:
    exit(1)

def predict_ssti(sentence):
    # Ensure the input is wrapped in a list
    return model.predict([sentence])[0]

@app.route('/note', methods=['POST'])
def check_note():
    note = request.json.get('note')

    # Predict S for the note
    prediction_ssti = predict_ssti(note)

    response = {
        "is_ssti": bool(prediction_ssti),
        "message": "No injection detected"
    }

    if response["is_ssti"]:
        response["message"] = "SSTI detected in note"
    return jsonify(response)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=4080)
