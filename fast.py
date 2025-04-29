import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from statsmodels.iolib.smpickle import load_pickle

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/predict_fao")
def predict_fao(n_steps: int):

    model_forecast = load_pickle("inflation/api/fao_model.pkl")

    forecast = model_forecast.forecast(steps=n_steps)

    y_train = pd.read_csv('inflation/api/y_train.csv')
    last_date = y_train.index[-1]
    last_date = pd.to_datetime(last_date)

    future_dates = pd.date_range(start=last_date + pd.offsets.MonthBegin(), periods=n_steps, freq='MS')

    forecast_df = pd.DataFrame({
        'date': future_dates,
        'predicted_value': forecast
    })

    return forecast_df

@app.get("/")
def root():
    return dict(greeting="Hello")
