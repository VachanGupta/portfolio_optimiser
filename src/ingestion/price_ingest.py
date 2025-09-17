import yfinance as yf
import pandas as pd
from pathlib import Path

# --- Configuration ---
TICKERS = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS']
START_DATE = '2020-01-01'
END_DATE = pd.Timestamp.today().strftime('%Y-%m-%d')
# Save to a new file to keep our original close prices file
SAVE_PATH = Path(__file__).parent.parent.parent / "data/raw/full_stock_data.csv"


def fetch_ohlcv_data(tickers, start, end, save_path):
    """
    Downloads full OHLCV data for a list of stock tickers
    from Yahoo Finance and saves it to a CSV file.
    """
    print(f"Downloading full OHLCV data for {tickers}...")
    
    # Download the full dataset. auto_adjust=False is needed to get all columns.
    # We will also group by ticker for a cleaner column structure.
    full_data = yf.download(tickers, start=start, end=end, auto_adjust=False, group_by='ticker')
    
    # Clean the data by dropping rows where all values are missing
    full_data.dropna(axis='index', how='all', inplace=True)

    save_path.parent.mkdir(parents=True, exist_ok=True)
    full_data.to_csv(save_path)
    
    print(f"Full data saved successfully to {save_path}!")
    print("--- First 5 rows of the data: ---")
    print(full_data.head())


if __name__ == '__main__':
    fetch_ohlcv_data(tickers=TICKERS, start=START_DATE, end=END_DATE, save_path=SAVE_PATH)