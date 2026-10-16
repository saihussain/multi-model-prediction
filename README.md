# Multi-Model Predictor

A small multi-model machine learning demo (Flask + scikit-learn) with a friendly local UI.
Includes:
- Iris classifier (4 features)
- Breast Cancer classifier (30 features)
- Local UI with probability display and CSV batch upload
- Easy to extend: add new models under `models/` as joblib `.pkl` files

## Quick start (local)

1. Create & activate a venv (Windows PowerShell):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
