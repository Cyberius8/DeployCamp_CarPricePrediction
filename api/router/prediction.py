from fastapi import APIRouter
from pydantic import ValidationError
from services.ml_service import MLService, CarPredictionRequestTest, CarPredictionRequestRFQ, CarPredictionResponse

router = APIRouter()
ml_service = MLService()

# convert json body request to dict
@router.post("/predict-test")
async def predict_test(request: CarPredictionRequestTest):
  data = request.dict()
  result = ml_service.predict(data, "test")
  return result

# convert json body request to dict
@router.post("/predict-rfq")
async def predict_rfq(request: CarPredictionRequestRFQ):
  data = request.dict()
  result = ml_service.predict(data, "rfq")
  return result
