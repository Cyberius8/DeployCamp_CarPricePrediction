import pickle
import pandas as pd
import mlflow
from pathlib import Path
from pydantic import BaseModel
from datetime import datetime

# Request model
class CarPredictionRequestTest(BaseModel):
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

# Request model for Random Forest Quantile Regression
class CarPredictionRequestRFQ(BaseModel):
    brand: int
    wheelbase: float
    carlength: float
    carwidth: float
    curbweight: float
    enginesize: float
    fuelsystem: int
    boreratio: float
    horsepower: float

# Response model  
class CarPredictionResponse(BaseModel):
    prediction: dict
    currency: str
    timestamp: str

class MLService:
  def __init__(self):
    mlflow.set_tracking_uri("https://dagshub.com/Cyberius8/DeployCamp_CarPricePrediction.mlflow")
    ml_flow_client = mlflow.MlflowClient()  
    
    self.model = mlflow.pyfunc.load_model(f"models:/QuantileRF/2")
    
  def predict(self, data, model_type):
    X = pd.DataFrame([data])

    if model_type == "rfq":
      predictions = self.model.predict(X).tolist()
      range_min = predictions[0][0]
      exact_value = predictions[1][0]
      range_max = predictions[2][0]
      confidence = 0.95

    if model_type == "test": 
      range_min = exact_value - 50000000
      exact_value = 500000000
      range_max = exact_value + 50000000
      confidence = 0

    return {
      "prediction": {
        "price_exact": int(exact_value),
        "price_range": {
          "min": int(range_min),
          "max": int(range_max)
        },
        "confidence": confidence
      },
      "currency": "IDR",
      "timestamp": datetime.now().isoformat()
    }
