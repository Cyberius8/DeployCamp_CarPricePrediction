import pickle
import pandas as pd
import mlflow
from pathlib import Path
from pydantic import BaseModel
from datetime import datetime

BRANDS = ["alfa_romeo", "audi", "bmw", "buick", "chevrolet", "dodge", "honda", "isuzu", "jaguar", "mazda", "mercury", "mitsubishi", "nissan", "peugeot", "plymouth", "porsche", "renault", "saab", "subaru", "toyota", "volkswagen", "volvo"]
FUELSYSTEMS = ["1bbl", "2bbl", "4bbl", "idi", "mfi", "mpfi", "spdi", "spfi"]

class CarPredictionRequest(BaseModel):
  fuelsystem: str
  brand: str
  wheelbase: float
  carlength: float
  carwidth: float
  curbweight: float
  enginesize: float
  boreratio: float
  horsepower: float

# Response model  
class PriceRange(BaseModel):
    min: int
    max: int

class Prediction(BaseModel):
    price_exact: int
    price_range: PriceRange
    confidence: float

class CarPredictionResponse(BaseModel):
    prediction: Prediction
    currency: str
    timestamp: datetime

class MLService:
  def __init__(self):
    mlflow.set_tracking_uri("https://dagshub.com/Cyberius8/DeployCamp_CarPricePrediction.mlflow")
    ml_flow_client = mlflow.MlflowClient()  
    self.model = mlflow.pyfunc.load_model(f"models:/QuantileRFOneHotEncoding/1")

  def one_hot_encode(self, data: CarPredictionRequest):
    data_encoded = {}
    for selected_brand in BRANDS:
      data_encoded[f"brand_{selected_brand}"] = 1 if data["brand"] == selected_brand else 0
    for selected_fuelsystem in FUELSYSTEMS:
      data_encoded[f"fuelsystem_{selected_fuelsystem}"] = 1 if data["fuelsystem"] == selected_fuelsystem else 0
    for other_data in ["wheelbase", "carlength", "carwidth", "curbweight", "enginesize", "boreratio", "horsepower"]:
      data_encoded[other_data] = data[other_data]
    return data_encoded

  def predict(self, data, model_type):
    data_encoded = self.one_hot_encode(data)
    X = pd.DataFrame([data_encoded])

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
