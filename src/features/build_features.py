import pandas as pd
import pandas_ta as ta
from pathlib import Path

# --- File Paths ---
RAW_DATA_PATH = Path(__file__).parent.parent.parent / "data/raw/full_stock_data.csv"
FEATURES_PATH = Path(__file__).parent.parent.parent / "data/processed/technical_features.csv"

def generate_features(raw_data_path, features_path):
    """
    Loads the raw OHLCV data and generates technical analysis features for each stock.
    Saves the combined features into a single CSV file.
    """
    print("Loading raw data...")
    # We need to read the header from the first two rows to handle the multi-level columns
    df = pd.read_csv(raw_data_path, header=[0, 1], index_col=0, parse_dates=True)
    
    print("Generating technical features...")
    all_features = []
    
    # Loop through each ticker in the columns
    tickers = df.columns.levels[0]
    for ticker in tickers:
        # Select the data for the current ticker
        stock_df = df[ticker].copy()
        
        # --- Calculate Technical Indicators using pandas_ta ---
        # Relative Strength Index (RSI)
        stock_df.ta.rsi(length=14, append=True)
        
        # Moving Average Convergence Divergence (MACD)
        stock_df.ta.macd(fast=12, slow=26, signal=9, append=True)
        
        # Bollinger Bands
        stock_df.ta.bbands(length=20, std=2, append=True)
        
        # Add the ticker name as a column for easier identification
        stock_df['Ticker'] = ticker
        
        all_features.append(stock_df)
        
    # Combine the features for all stocks into a single DataFrame
    features_df = pd.concat(all_features)
    
    # Clean up any resulting NaN values
    features_df.dropna(inplace=True)
    
    # Save the features to the processed data folder
    features_path.parent.mkdir(parents=True, exist_ok=True)
    features_df.to_csv(features_path)
    
    print(f"Features saved successfully to {features_path}!")
    print("--- Sample of generated features for one stock: ---")
    print(features_df.head())

if __name__ == "__main__":
    generate_features(raw_data_path=RAW_DATA_PATH, features_path=FEATURES_PATH)