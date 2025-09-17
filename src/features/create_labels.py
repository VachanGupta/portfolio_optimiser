import pandas as pd
from pathlib import Path

# --- Configuration ---
HORIZON_DAYS = 5  # We are predicting 5 days into the future
FEATURES_PATH = Path(__file__).parent.parent.parent / "data/processed/final_features.csv"
LABELED_DATA_PATH = Path(__file__).parent.parent.parent / "data/processed/labeled_features.csv"

def generate_labels(features_path, labeled_path, horizon):
    """
    Creates the target label for our model.
    The label is 1 if the stock price increases over the horizon, and 0 otherwise.
    """
    print(f"Loading features from {features_path}...")
    df = pd.read_csv(features_path, parse_dates=['Date'])

    print(f"Generating labels for a {horizon}-day horizon...")
    
    # --- The Core Logic ---
    # We group by each stock, so the shift operation doesn't look at the wrong stock's future price.
    # .shift(-horizon) pulls the value from 'horizon' rows in the future up to the current row.
    future_price = df.groupby('Ticker')['Close'].shift(-horizon)
    
    # Calculate the future return
    df['future_return'] = (future_price - df['Close']) / df['Close']
    
    # Create the binary target label: 1 for up, 0 for down/same
    df['target'] = (df['future_return'] > 0).astype(int)
    
    # --- Clean up ---
    # The last 'horizon' rows for each stock will have no future price, so their labels are NaN.
    # We drop these rows as we cannot use them for training.
    df.dropna(subset=['future_return'], inplace=True)
    
    labeled_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(labeled_path, index=False)
    
    print(f"Labeled data saved successfully to {labeled_path}")
    print("--- Sample of labeled data (notice the new 'future_return' and 'target' columns): ---")
    print(df[['Date', 'Ticker', 'Close', 'future_return', 'target']].head())
    

if __name__ == "__main__":
    generate_labels(features_path=FEATURES_PATH,
                    labeled_path=LABELED_DATA_PATH,
                    horizon=HORIZON_DAYS)