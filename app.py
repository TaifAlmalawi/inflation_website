import streamlit as st
import pandas as pd
from statsmodels.iolib.smpickle import load_pickle
import matplotlib.pyplot as plt
import numpy as np

st.sidebar.markdown("""
# 📈 Inflation Forecast App

🌾 About FAO Data

This forecast specific to Saudi Arabia is based on food price data collected by the Food and Agriculture Organization (FAO), which monitors global food markets and trends.
""")

# Input section
n_steps = st.sidebar.text_input('How many months do you want to predict?🤔', 0)
st.write('The current number of months is ', int(n_steps))

# Load model
model_forecast = load_pickle("fao_model.pkl")

# Forecast section
if st.sidebar.button('Predict the future: 🔮'):

    if int(n_steps) > 0:
        forecast = model_forecast.forecast(steps=int(n_steps))

        y_train = pd.read_csv('y_train.csv', index_col=0)
        y_train.index = pd.to_datetime(y_train.index)

        last_date = y_train.index[-1]
        future_dates = pd.date_range(start=last_date + pd.offsets.MonthBegin(), periods=int(n_steps), freq='MS')

        forecast_values = forecast if not isinstance(forecast, np.ndarray) else forecast.tolist()

        forecast_df = pd.DataFrame({
            'predicted_value': forecast_values
        }, index=future_dates)
        forecast_df.index.name = 'date'

        st.table(forecast_df)
        st.line_chart(forecast_df)

        # Show instruction under the button
        st.markdown('Click the **"Predict the future 🔮"** button again to update the forecast.')
    else:
        st.write('I\'m sorry... Please enter a valid number of steps.')

st.sidebar.markdown('Click the **"Predict the future 🔮"** button to see the forecast')

# === New Section: CPI Forecast Visualization ===
st.markdown("---")
st.header("📊 CPI Forecast Visualization")

st.markdown("""
This section provides a visualization of CPI (Consumer Price Index) forecasts.
The images below show expected trends in consumer prices in Saudi Arabia based on historical CPI data.
""")

st.image("cpi.png", caption="CPI Forecast Trend - Model A")
