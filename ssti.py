from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from waitress import serve

app = Flask(__name__)
CORS(app)  # Allow Cross-Origin Resource Sharing

# Load the best model
model = joblib.load('SSTI.pkl')

def predict_ssti(sentences):
    return model.predict(sentences)[0]

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
