from fastapi import APIRouter
from pydantic import ValidationError
from services.ml_service import MLService, CarPredictionRequest, CarPredictionResponse

router = APIRouter()
ml_service = MLService()

# convert json body request to dict
@router.post("/predict", response_model=CarPredictionResponse)
async def predict(request: CarPredictionRequest):
  data = request.dict()
  result = ml_service.predict(data)
  return result
