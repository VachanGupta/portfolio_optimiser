import pandas as pd
from pathlib import Path

# --- File Paths ---
TECH_FEATURES_PATH = Path(__file__).parent.parent.parent / "data/processed/technical_features.csv"
SENTIMENT_FEATURES_PATH = Path(__file__).parent.parent.parent / "data/processed/sentiment_features.csv"
FINAL_FEATURES_PATH = Path(__file__).parent.parent.parent / "data/processed/final_features.csv"

def combine_features(tech_path, sentiment_path, final_path):
    """
    Combines technical and sentiment features into a single master feature set.
    """
    print("Loading technical and sentiment features...")
    tech_features = pd.read_csv(tech_path, parse_dates=['Date'])
    sentiment_features = pd.read_csv(sentiment_path, parse_dates=['Date'])
    
    print("Merging feature sets...")
    # Perform a 'left' merge. This keeps all rows from the technical features DataFrame
    # and adds sentiment scores where the 'Date' and 'Ticker' match.
    final_df = pd.merge(tech_features, sentiment_features, on=['Date', 'Ticker'], how='left')
    
    # --- Handle Missing Sentiment Data ---
    # For dates where we have no news, the sentiment_score will be NaN (Not a Number).
    # We will fill these missing values with 0, assuming a neutral sentiment for those days.
    final_df['sentiment_score'].fillna(0, inplace=True)
    
    # Sort data just to be sure
    final_df.sort_values(by=['Ticker', 'Date'], inplace=True)
    
    # Save the final master feature set
    final_path.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(final_path, index=False)
    
    print(f"Final combined features saved to {final_path}")
    print("--- Sample of final features: ---")
    print(final_df.head())
    print("\n--- A look at a recent date to confirm sentiment scores are present: ---")
    print(final_df.tail())

if __name__ == "__main__":
    combine_features(tech_path=TECH_FEATURES_PATH,
                     sentiment_path=SENTIMENT_FEATURES_PATH,
                     final_path=FINAL_FEATURES_PATH)