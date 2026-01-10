import os
import pickle
import pandas as pd
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# ==================================
# Load model using absolute path
# ==================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_rf_pipeline.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# ==================================
# Home
# ==================================
@app.route("/")
def home():
    return render_template("home.html")

# ==================================
# Predict
# ==================================
@app.route("/predict", methods=["POST"])
def predict():
    input_data = {
        "CRIM": float(request.form["CRIM"]),
        "ZN": float(request.form["ZN"]),
        "INDUS": float(request.form["INDUS"]),
        "CHAS": str(request.form["CHAS"]),   # IMPORTANT
        "NOX": float(request.form["NOX"]),
        "RM": float(request.form["RM"]),
        "AGE": float(request.form["AGE"]),
        "DIS": float(request.form["DIS"]),
        "RAD": str(request.form["RAD"]),     # IMPORTANT
        "TAX": float(request.form["TAX"]),
        "PTRATIO": float(request.form["PTRATIO"]),
        "B": float(request.form["B"]),
        "LSTAT": float(request.form["LSTAT"])
    }

    df = pd.DataFrame([input_data])
    prediction = model.predict(df)[0]

    return jsonify({"price": round(float(prediction), 2)})

if __name__ == "__main__":
    app.run(debug=True)