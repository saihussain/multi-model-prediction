# app.py
from flask import Flask, request, jsonify, render_template

import joblib
import numpy as np
import os

app = Flask(__name__)

# Load only models that exist (safe)
MODELS = {}
MODEL_META = {}

if os.path.exists("models/iris_model.pkl"):
    MODELS["iris"] = joblib.load("models/iris_model.pkl")
    MODEL_META["iris"] = {
        "type": "classifier",
        "feature_count": 4,
        "class_names": ["setosa", "versicolor", "virginica"]
    }

if os.path.exists("models/breast_cancer.pkl"):
    MODELS["breast_cancer"] = joblib.load("models/breast_cancer.pkl")
    MODEL_META["breast_cancer"] = {
        "type": "classifier",
        "feature_count": 30,
        "class_names": ["malignant", "benign"]
    }

if not MODELS:
    raise RuntimeError("No models found in models/ folder. Add iris_model.pkl and/or breast_cancer.pkl")

from flask import render_template  # add at top if not already imported

@app.route("/")
def index():
    # serve the UI page (templates/index.html)
    return render_template("index.html")
@app.route("/models", methods=["GET"])
def list_models():
    return jsonify({"models": list(MODELS.keys())})


@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(force=True)
    model_name = payload.get("model")
    features = payload.get("features")

    if model_name not in MODELS:
        return jsonify({"error": f"model '{model_name}' not found", "available": list(MODELS.keys())}), 400

    meta = MODEL_META[model_name]
    expected_len = meta["feature_count"]
    if not isinstance(features, list):
        return jsonify({"error": "features must be a list of numbers"}), 400
    if len(features) != expected_len:
        return jsonify({"error": f"expected {expected_len} features for model '{model_name}', got {len(features)}"}), 400

    try:
        X = np.array(features, dtype=float).reshape(1, -1)
    except Exception as e:
        return jsonify({"error": "invalid feature values: " + str(e)}), 400

    model = MODELS[model_name]
    pred = model.predict(X)[0]
    probs = model.predict_proba(X).tolist() if hasattr(model, "predict_proba") else None

    # map numeric preds to class names if possible
    class_name = None
    if isinstance(pred, (int, np.integer)):
        names = meta.get("class_names")
        class_name = names[int(pred)] if names and int(pred) < len(names) else str(int(pred))
    else:
        class_name = str(pred)

    return jsonify({
        "model": model_name,
        "predicted": int(pred) if isinstance(pred, (int, np.integer)) else class_name,
        "class_name": class_name,
        "probabilities": probs
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
