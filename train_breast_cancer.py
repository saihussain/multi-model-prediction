# train_breast_cancer.py
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# 1. load data
data = load_breast_cancer()
X, y = data.data, data.target  # y: 0=malignant, 1=benign (check dataset mapping)

# 2. split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. build pipeline (scaler + rf)
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("rf", RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1))
])

# 4. train
pipeline.fit(X_train, y_train)

# 5. evaluate
y_pred = pipeline.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=data.target_names))

# 6. save model
os.makedirs("models", exist_ok=True)
joblib.dump(pipeline, "models/breast_cancer.pkl")
print("Saved model to models/breast_cancer.pkl")
