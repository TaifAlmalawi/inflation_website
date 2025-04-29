import streamlit as st
import pandas as pd
from statsmodels.iolib.smpickle import load_pickle
import matplotlib.pyplot as plt

st.markdown("""
    # Inflation Prediction

    ## many levels of subtitles

    **bold** or *italic* text with [links](http://github.com/streamlit) and:
    - bullet points
""")

n_steps = st.text_input('Insert a number of steps:')

st.write('The current number of steps is ', int(n_steps))

model_forecast = load_pickle("fao_model.pkl")

if st.button('Predict the future: 🔮'):
    forecast = model_forecast.forecast(steps=int(n_steps))

    y_train = pd.read_csv('y_train.csv')
    last_date = y_train.index[-1]
    last_date = pd.to_datetime(last_date)

    future_dates = pd.date_range(start=last_date + pd.offsets.MonthBegin(), periods=int(n_steps), freq='MS')

    forecast_df = pd.DataFrame({
        'date': future_dates,
        'predicted_value': forecast
    })

    st.table(forecast_df)

