from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List
class PredictionRequest(BaseModel):

    ph: float
    hardness: float
    solids: float
    chloramines: float
    sulfate: float
    conductivity: float
    organic_carbon: float
    trihalomethanes: float
    turbidity: float
    potability: int
    class Config:
        extra = "forbid"

class PredictionResponse(BaseModel):
    prediction: str
    probability: float


class WaterSampleCreate(PredictionRequest):
    pass

class WaterSampleResponse(PredictionRequest):
    id: int
    prediction: str
    probability: float

    cleaning_suggestions: Optional[List[str]] = None
    developing_suggestions: Optional[List[str]] = None

    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True
