import pandas as pd
import re
from pathlib import Path

RAW_CSV = Path(__file__).resolve().parent.parent / "data" / "water_potability.csv"
OUTPUT_CSV = Path(__file__).resolve().parent.parent / "data" / "cleaned_water_data.csv"

COLUMN_MAP = {
    "ph": "ph",
    "hardness": "hardness",
    "solids": "solids",
    "chloramines": "chloramines",
    "sulfate": "sulfate",
    "conductivity": "conductivity",
    "organic_carbon": "organic_carbon",
    "trihalomethanes": "trihalomethanes",
    "turbidity": "turbidity",
    "potability": "potability",
}


def clean_column_name(column_name: str) -> str:
    cleaned = str(column_name).strip().lower()
    cleaned = cleaned.replace(" ", "_")
    cleaned = re.sub(r"[()\\/\+]", "", cleaned)
    return COLUMN_MAP.get(cleaned, cleaned)


def main():
    df = pd.read_csv(RAW_CSV)
    df.columns = [clean_column_name(col) for col in df.columns]

    numeric_cols = list(COLUMN_MAP.values())
    numeric_cols.remove("potability")

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        else:
            df[col] = 0.0

    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    if "potability" in df.columns:
        df["potability"] = pd.to_numeric(df["potability"], errors="coerce")
        df = df.dropna(subset=["potability"])
        df["potability"] = df["potability"].astype(int)

    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Clean dataset saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
