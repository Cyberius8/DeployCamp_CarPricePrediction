from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from router.prediction import router
from datetime import datetime

# MLFlow
import mlflow
mlflow.set_tracking_uri("https://dagshub.com/Cyberius8/DeployCamp_CarPricePrediction.mlflow")
ml_flow_client = mlflow.MlflowClient()  

# FastAPI
app = FastAPI()
app.include_router(router)

# CORS Middleware
origins = [
  "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# custom error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
  return JSONResponse(
    status_code=400,
    content=jsonable_encoder({
      "message": "error 400 - input data is not valid",
      "timestamp": datetime.now().isoformat()
    }),
  )

@app.get(
  "/",
  response_model=dict,
  summary="Welcome page for API",
  response_description="Welcome message"
)
def hello():
    return {"message": "hello this is car price predictor using FastAPI"}

@app.get(
  "/health",
  response_model=dict,
  summary="Health check endpoint",
  response_description="Health status of the FastAPI application"
)
def health_check():
    return {"status": "FastAPI is ready"}
