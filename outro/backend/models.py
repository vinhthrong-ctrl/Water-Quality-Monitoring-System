from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class Water_Data(Base):
    __tablename__ = "Water_Data"

    id = Column(Integer, primary_key=True, index=True,  autoincrement=True)

    ph = Column(Float)
    hardness = Column(Float)
    solids = Column(Float)
    chloramines = Column(Float)
    sulfate = Column(Float)
    conductivity = Column(Float)
    organic_carbon = Column(Float)
    trihalomethanes = Column(Float)
    turbidity = Column(Float)
    probability = Column(Float)
    potability = Column(Integer)
    prediction = Column(String, nullable=False)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())