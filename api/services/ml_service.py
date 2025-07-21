import pickle
import pandas as pd
from pathlib import Path
from pydantic import BaseModel
from datetime import datetime

# Request model
class CarPredictionRequest(BaseModel):
    fueltype: int
    aspiration: int
    doornumber: int
    carbody: int
    drivewheel: int
    enginelocation: int
    wheelbase: float
    carlength: float
    carwidth: float
    carheight: float
    curbweight: float
    enginetype: int
    cylindernumber: int
    enginesize: float
    fuelsystem: int
    boreratio: float
    stroke: float
    compressionratio: float
    horsepower: float
    peakrpm: float
    citympg: float
    highwaympg: float
    brand: int

# Response model  
class CarPredictionResponse(BaseModel):
    prediction: dict
    currency: str
    timestamp: str

class MLService:
  def __init__(self):
    # model_path = Path(__file__)
    # with open(model_path, "rb") as f:
      # self.model = pickle.load(f)
    pass
    
  def predict(self, data):
    X = pd.DataFrame([data])
    # prediction = self.model.predict(X)[0]
    # proba = self.model.predict_proba(X)[0]
    exact_value = 500000000
    range_min = exact_value - 50000000
    range_max = exact_value + 50000000
    confidence = 0.9
        
    return {
      "prediction": {
        "price_exact": int(exact_value),
        "price_range": {
          "min": range_min,
          "max": range_max
        },
        "confidence": round(confidence, 2)
      },
      "currency": "IDR",
      "timestamp": datetime.now().isoformat()
    }
