from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from waitress import serve
from utils import custom_tokenizer

app = Flask(__name__)
CORS(app)  # Allow Cross-Origin Resource Sharing

# Load the best model (without passing globals)
model = joblib.load('SSTI.pkl')

def predict_ssti(sentence):
    # Ensure the input is a list of strings even for a single sentence
    return model.predict([sentence])[0]

@app.route('/note', methods=['POST'])
def check_note():
    data = request.get_json(force=True)
    notes = data.get('note')

    if not isinstance(notes, list):
        return jsonify({
            "error": "Invalid input",
            "message": "Expected 'note' to be a list of strings"
        }), 400

    # Predict SSTI for each note
    predictions = [predict_ssti(note) for note in notes]

    response = {
        "results": [
            {
                "note": note,
                "is_ssti": bool(pred),
                "message": "SSTI detected in note" if pred else "No injection detected"
            } for note, pred in zip(notes, predictions)
        ]
    }

    return jsonify(response)

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=4080)
