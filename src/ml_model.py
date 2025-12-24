import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os


MODEL_PATH = "model/random_forest_model.pkl"


def train_model(data: pd.DataFrame):

    df = data.copy()

    # Make sure required columns exist
    required = ["Close", "SMA20", "SMA50", "EMA20", "signal"]
    if not all(col in df.columns for col in required):
        raise ValueError("Dataset missing required indicator columns.")

    # Create target (next-day signal prediction)
    df["target"] = df["signal"].shift(-1)
    df.dropna(inplace=True)

    X = df[["Close", "SMA20", "SMA50", "EMA20"]]
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))

    # Save trained model
    os.makedirs("model", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return accuracy, MODEL_PATH


def load_model():
    import joblib
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


def predict_signal(latest_row):
    model = load_model()
    if model is None:
        return None, None  # No model yet

    X_live = [[latest_row["Close"], latest_row["SMA20"], latest_row["SMA50"], latest_row["EMA20"]]]

    # Predicted class
    pred_class = model.predict(X_live)[0]

    # Confidence score
    probs = model.predict_proba(X_live)[0]
    confidence = max(probs)  # highest class probability

    return pred_class, confidence

    X_live = [[latest_row["Close"], latest_row["SMA20"], latest_row["SMA50"], latest_row["EMA20"]]]
    return model.predict(X_live)[0]
