import streamlit as st
import pandas as pd
from pathlib import Path
import joblib

# --- Configuration ---
st.set_page_config(page_title="Intelligent Portfolio Optimizer", layout="wide")

# --- File Paths ---
# Adjust paths to be relative to the script location
BASE_DIR = Path(__file__).parent.parent
MODEL_PATH = BASE_DIR / "models/xgb_model.joblib"
DATA_PATH = BASE_DIR / "data/processed/labeled_features.csv"

# --- Load Model and Data ---
@st.cache_data # Cache the data so it doesn't reload on every interaction
def load_data(data_path):
    return pd.read_csv(data_path, parse_dates=['Date'])

@st.cache_resource # Cache the model so it doesn't reload
def load_model(model_path):
    return joblib.load(model_path)

df = load_data(DATA_PATH)
model = load_model(MODEL_PATH)

# --- UI Layout ---
st.title("🤖 Intelligent Stock Portfolio Optimizer")
st.write("""
This dashboard uses a trained XGBoost model to predict the 5-day price movement 
for a pre-selected portfolio of Indian stocks. The model was trained on historical
price data, technical indicators, and news sentiment scores.
""")

st.header("Latest Predictions", divider='rainbow')

# --- Prediction Logic ---
# Get the most recent data point for each ticker
latest_data = df.loc[df.groupby('Ticker')['Date'].idxmax()]

if st.button("Run Prediction for Today", type="primary"):
    with st.spinner("Making predictions..."):
        # Prepare features for the model
        features_to_drop = ['Date', 'Ticker', 'future_return', 'target', 
                            'Open', 'High', 'Low', 'Adj Close', 'Volume']
        X_predict = latest_data.drop(columns=features_to_drop)
        
        # Make predictions and get probabilities
        predictions = model.predict(X_predict)
        probabilities = model.predict_proba(X_predict)
        
        # Add results to the dataframe
        latest_data['Prediction'] = predictions
        latest_data['Confidence'] = probabilities.max(axis=1)
        
        # Display results in cards
        cols = st.columns(len(latest_data))
        for i, row in enumerate(latest_data.itertuples()):
            with cols[i]:
                st.metric(label=f"**{row.Ticker}**", 
                          value="UP 📈" if row.Prediction == 1 else "DOWN 📉",
                          delta=f"Confidence: {row.Confidence:.2%}")
                st.write(f"Last Close: ₹{row.Close:.2f}")
                st.write(f"Date: {row.Date.date()}")
else:
    st.info("Click the button to get the latest 5-day price predictions.")