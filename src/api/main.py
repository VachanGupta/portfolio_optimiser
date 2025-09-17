from fastapi import FastAPI
import pandas as pd
from pathlib import Path
import joblib

# --- Initialize FastAPI app ---
app = FastAPI(title="Portfolio Optimizer API")

# --- Load Model and Data ---
# These are loaded once when the API starts up for efficiency
BASE_DIR = Path(__file__).parent.parent.parent
MODEL_PATH = BASE_DIR / "models/xgb_model.joblib"
DATA_PATH = BASE_DIR / "data/processed/labeled_features.csv"

model = joblib.load(MODEL_PATH)
df = pd.read_csv(DATA_PATH, parse_dates=['Date'])

# --- API Endpoint ---
@app.post("/predict")
def predict_stocks():
    """
    Loads the latest data for all tickers, makes a prediction, 
    and returns the results as JSON.
    """
    latest_data = df.loc[df.groupby('Ticker')['Date'].idxmax()]
    
    features_to_drop = ['Date', 'Ticker', 'future_return', 'target', 
                        'Open', 'High', 'Low', 'Adj Close', 'Volume']
    X_predict = latest_data.drop(columns=features_to_drop)
    
    # Get predictions and probabilities
    predictions = model.predict(X_predict)
    probabilities = model.predict_proba(X_predict)
    
    # Format the results
    latest_data['prediction'] = predictions
    latest_data['confidence'] = probabilities.max(axis=1)
    
    results = latest_data[['Ticker', 'Date', 'Close', 'prediction', 'confidence']].to_dict('records')
    
    return {"predictions": results}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Portfolio Optimizer API"}