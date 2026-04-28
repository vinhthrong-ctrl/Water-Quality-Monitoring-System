import re
from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Paths
MODEL_PATH = Path(__file__).resolve().parent / "model" / "wqms_model.joblib"

WATER_SAMPLE_CSV = Path(__file__).resolve().parent.parent / "data" / "Water_Data.csv"
CLEANED_SAMPLE_CSV = Path(__file__).resolve().parent.parent / "data" / "cleaned_water_data.csv"
RAW_SAMPLE_CSV = Path(__file__).resolve().parent.parent / "data" / "water_potability.csv"

SAMPLE_CSV = (
    WATER_SAMPLE_CSV if WATER_SAMPLE_CSV.exists()
    else CLEANED_SAMPLE_CSV if CLEANED_SAMPLE_CSV.exists()
    else RAW_SAMPLE_CSV
)

FEATURE_COLUMNS = [
    "ph",
    "hardness",
    "solids",
    "chloramines",
    "sulfate",
    "conductivity",
    "organic_carbon",
    "trihalomethanes",
    "turbidity",
]

TARGET_COLUMN = "potability"


# -------------------------
# CLEAN COLUMN NAMES
# -------------------------
def clean_column_name(name: str) -> str:
    name = str(name).lower().strip()
    name = name.replace(" ", "_")
    name = re.sub(r"[()\\/\+\u00b5]", "", name)

    mappings = {
        "organiccarbon": "organic_carbon",
        "trihalomethanes": "trihalomethanes",
        "conductivity": "conductivity",
    }

    return mappings.get(name, name)


# -------------------------
# LOAD DATA
# -------------------------
def load_training_data(csv_path: str = None) -> pd.DataFrame:
    path = Path(csv_path) if csv_path else SAMPLE_CSV
    df = pd.read_csv(path)

    # Clean column names
    df.columns = [clean_column_name(col) for col in df.columns]

    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Missing target column: {TARGET_COLUMN}")

    # Convert target
    df[TARGET_COLUMN] = pd.to_numeric(df[TARGET_COLUMN], errors="coerce")
    df = df.dropna(subset=[TARGET_COLUMN])

    # Ensure all features exist
    for col in FEATURE_COLUMNS:
        if col not in df.columns:
            df[col] = df[col].median()
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fill missing values
    df[FEATURE_COLUMNS] = df[FEATURE_COLUMNS].fillna(df[FEATURE_COLUMNS].median())
    df[TARGET_COLUMN] = df[TARGET_COLUMN].astype(int)

    return df


# -------------------------
# TRAIN MODEL
# -------------------------
def train_and_save(csv_path: str = None, model_path: str = None) -> dict:
    df = load_training_data(csv_path)

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    # Models
    candidates = {
        "logistic_regression": Pipeline([
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=500, solver="liblinear"))
        ]),

        "decision_tree": DecisionTreeClassifier(
            random_state=42,
            max_depth=6
        ),

        "random_forest": RandomForestClassifier(
            n_estimators=300,
            max_depth=12,
            random_state=42,
            class_weight="balanced"
        ),
    }

    best_model = None
    best_score = -1
    best_name = ""

    for name, model in candidates.items():
        model.fit(X_train, y_train)
        score = accuracy_score(y_test, model.predict(X_test))

        print(f"{name}: {score:.4f}")

        if score > best_score:
            best_score = score
            best_model = model
            best_name = name

    # Save model
    model_dest = Path(model_path) if model_path else MODEL_PATH
    model_dest.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, model_dest)

    return {
        "model_path": str(model_dest),
        "accuracy": best_score,
        "type": best_name,
    }


# -------------------------
# LOAD MODEL
# -------------------------
def load_model(model_path: str = None):
    path = Path(model_path) if model_path else MODEL_PATH

    if not path.exists():
        raise FileNotFoundError(
            f"Model not found at {path}. Run training first."
        )

    return joblib.load(path)


# -------------------------
# PREDICT
# -------------------------
def predict_sample(model, sample: dict) -> dict:
    features = []

    for column in FEATURE_COLUMNS:
        value = sample.get(column, 0.0)
        try:
            value = float(value)
        except (TypeError, ValueError):
            value = 0.0
        features.append(value)

    # Get probability
    if hasattr(model, "predict_proba"):
        probability = model.predict_proba([features])[0][1]
    else:
        probability = float(model.predict([features])[0])

    # Better interpretation (not rigid)
    if probability >= 0.7:
        label = "Safe"
    elif probability >= 0.4:
        label = "Moderate"
    else:
        label = "Unsafe"

    return {
        "prediction": label,
        "probability": round(float(probability), 4),
    }


# -------------------------
# RUN TRAINING
# -------------------------
if __name__ == "__main__":
    try:
        print("Starting model training...\n")

        result = train_and_save()

        print("\nTraining completed")
        print(f"Model saved at: {result['model_path']}")
        print(f"Accuracy: {result['accuracy']:.3f}")
        print(f"Best model: {result['type']}")

    except Exception as e:
        print("\nTraining failed")
        print(f"Error: {str(e)}")