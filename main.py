from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

# Load model, scaler, and list of columns to scale
model = joblib.load("ml/model.pkl")
scaler = joblib.load("ml/pipeline.pkl")
scale_columns = joblib.load("ml/col_piped.pkl")  # ['age', 'heart rate']
feature_columns = joblib.load("ml/features.pkl")  # List of all features

# Initialize FastAPI app
app = FastAPI()

# Define the request schema
class HeartDiseasePredictionRequest(BaseModel):
    age: int
    sex: int
    highbp: int
    highchol: int
    heart_rate: float
    previous_heart_problems: int
    smoker: int
    stroke: int
    diabetes: int
    physactivity: int
    hvyalcoholconsump: int
    anyhealthcare: int

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
    # Convert the input data to a DataFrame
    input_data = pd.DataFrame([data.dict()])

    # Apply scaling to specific columns only
    input_data[scale_columns] = scaler.transform(input_data[scale_columns])

    # Convert the DataFrame to a numpy array in the correct feature order
    input_data_array = input_data[feature_columns].values

    # Make prediction
    prediction = model.predict(input_data_array)[0]
    probability = model.predict_proba(input_data_array)[0][1]  # Probability of heart disease

    # Return the prediction result
    return HeartDiseasePredictionResponse(prediction=int(prediction), probability=float(probability))
