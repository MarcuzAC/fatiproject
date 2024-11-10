from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

# Load saved model, scaler, and column names
model = joblib.load("ml/model.pkl")
scaler = joblib.load("ml/pipeline.pkl")
scaler_col = joblib.load("ml/col_piped.pkl")
feature_columns = joblib.load("ml/features.pkl")

# Initialize the FastAPI app
app = FastAPI()

# Define the request schema
class HeartDiseasePredictionRequest(BaseModel):
    age: float
    heart_rate: float

# Define the response schema
class HeartDiseasePredictionResponse(BaseModel):
    prediction: int
    probability: float

# Health check route
@app.get("/")
def read_root():
    return {"message": "Heart Disease Prediction Model API"}

# Prediction route
@app.post("/predict", response_model=HeartDiseasePredictionResponse)
def predict(data: HeartDiseasePredictionRequest):
    # Create a numpy array from input data
    input_data = np.array([[data.age, data.heart_rate]])

    # Scale input data
    input_data_scaled = scaler.transform(input_data)

    # Make prediction
    prediction = model.predict(input_data_scaled)[0]
    probability = model.predict_proba(input_data_scaled)[0][1]  # Probability of heart disease

    # Return the prediction result
    return HeartDiseasePredictionResponse(prediction=int(prediction), probability=float(probability))

# Error handling for invalid routes
@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    return {"error": exc.detail}
