from typing import Dict, Optional

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import models
from database import supabase, Base, engine, get_db
from schemas import PredictionRequest, PredictionResponse, WaterSampleCreate, WaterSampleResponse
from ml import load_model, predict_sample

app = FastAPI(
    title="Water Quality Monitoring System",
    description="FastAPI backend for water quality prediction using water potability analysis.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


def _parse_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def sample_to_dict(sample: models.Water_Data) -> Dict:
    return {
        "id": sample.id,
        "ph": sample.ph,
        "hardness": sample.hardness,
        "solids": sample.solids,
        "chloramines": sample.chloramines,
        "sulfate": sample.sulfate,
        "conductivity": sample.conductivity,
        "organic_carbon": sample.organic_carbon,
        "trihalomethanes": sample.trihalomethanes,
        "turbidity": sample.turbidity,
        "potability": sample.potability,
        "probability": sample.probability,
        "prediction": sample.prediction,
    }


@app.get("/")
def root():
    response = supabase.table("Water_Data").select("*").execute()
    return response.data

@app.get("/samples")
def get_samples():
    response = supabase.table("Water_Data").select("*").execute()
    return response.data

@app.get("/unsafe-areas", tags=["analysis"])
def get_unsafe_areas(limit: int = 100):
    response = supabase.table("Water_Data").select("*").execute()
    data = response.data

    unsafe = [s for s in data if s.get("prediction") == "Unsafe"]

    return {
        "total_samples": len(data),
        "unsafe_count": len(unsafe),
        "unsafe_rate": round(len(unsafe) / len(data), 4) if data else 0,
        "unsafe_samples": unsafe[:limit],
    }

@app.post("/predict", response_model=PredictionResponse, tags=["prediction"])
def predict(request: PredictionRequest):
    result = predict_sample(model, request.dict())
    return PredictionResponse(**result)


@app.post("/add-sample", tags=["samples"])
def add_sample(request: WaterSampleCreate):
    samples = request.dict()
    prediction = predict_sample(model, samples)

    data = {
        **samples,
        "probability": prediction["probability"],
        "prediction": prediction["prediction"],
    }

    response = supabase.table("Water_Data").insert(data).execute()

    return response.data    
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    return db_sample
