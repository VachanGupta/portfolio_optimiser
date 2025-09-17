import streamlit as st
import pandas as pd
import requests # For making API requests

# --- Configuration ---
st.set_page_config(page_title="Intelligent Portfolio Optimizer", layout="wide")

# The URL of our FastAPI backend
# 'api' is the name we will give our service in Docker Compose
API_URL = "http://api:8000/predict" 

# --- UI Layout ---
st.title("🤖 Intelligent Stock Portfolio Optimizer")
st.write("""
This dashboard uses a trained XGBoost model to predict the 5-day price movement 
for a pre-selected portfolio of Indian stocks. The predictions are served from a separate FastAPI backend.
""")

st.header("Latest Predictions", divider='rainbow')

if st.button("Run Prediction for Today", type="primary"):
    with st.spinner("Sending request to the model API..."):
        try:
            response = requests.post(API_URL)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            results = response.json()['predictions']
            results_df = pd.DataFrame(results)
            
            # Display results in cards
            cols = st.columns(len(results_df))
            for i, row in enumerate(results_df.itertuples()):
                with cols[i]:
                    st.metric(label=f"**{row.Ticker}**", 
                              value="UP 📈" if row.prediction == 1 else "DOWN 📉",
                              delta=f"Confidence: {row.confidence:.2%}")
                    st.write(f"Last Close: ₹{row.Close:.2f}")
                    st.write(f"Date: {pd.to_datetime(row.Date).date()}")

        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to the API. Make sure the backend is running. Error: {e}")

else:
    st.info("Click the button to get the latest 5-day price predictions.")