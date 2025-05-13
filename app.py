import pandas as pd
from flask import Flask, request, jsonify

# Create Flask API
app = Flask(__name__)

@app.route("/get_patient", methods=["GET"])
def get_patient():
    # Load Fake EHR Data from Google sheet link
    file_path = "https://docs.google.com/spreadsheets/d/1GjPej9sUisGZbpE0psl3FD_PMZPJD5XlW3NNmGX0y4s/gviz/tq?tqx=out:csv"
    fake_EHR = pd.read_csv(file_path)

    """Fetch patient data by ID"""
    patient_id = request.args.get("patient_id")  # Get patient ID from request
    if not patient_id:
        return jsonify({"error": "No patient_id provided"}), 400

    # Convert patient_id to integer
    try:
        patient_id = int(patient_id)
    except ValueError:
        return jsonify({"error": "Invalid patient_id format"}), 400  # Handle conversion error

    patient_data = fake_EHR[fake_EHR["patient_id"] == patient_id]
    if patient_data.empty:
        return jsonify({"error": "Patient not found"}), 404

    # Convert DataFrame row to JSON
    return jsonify(patient_data.to_dict(orient="records")[0])

if __name__ == "__main__":
    app.run()
