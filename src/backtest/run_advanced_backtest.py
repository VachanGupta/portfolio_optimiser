import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import matplotlib.pyplot as plt

# --- File Paths ---
LABELED_DATA_PATH = Path(__file__).parent.parent.parent / "data/processed/labeled_features.csv"
MODEL_PATH = Path(__file__).parent.parent.parent / "models/xgb_model.joblib"
PLOT_SAVE_PATH = Path(__file__).parent.parent.parent / "advanced_backtest_performance.png"

def run_advanced_backtest(labeled_data_path, model_path, plot_save_path):
    """
    Runs a confidence-weighted backtest simulation on the test data.
    """
    print("Loading model and data for advanced backtest...")
    model = joblib.load(model_path)
    df = pd.read_csv(labeled_data_path, parse_dates=['Date'])
    
    test_df = df[df['Date'] >= '2025-01-01'].copy()
    
    features_to_drop = ['Date', 'Ticker', 'future_return', 'target', 
                        'Open', 'High', 'Low', 'Adj Close', 'Volume']
    X_test = test_df.drop(columns=features_to_drop)
    
    print("Generating prediction probabilities for the test period...")
    # Get the probability of the "UP" class (which is the second column)
    probabilities = model.predict_proba(X_test)[:, 1]
    test_df['confidence'] = probabilities
    
    # --- Simulate Advanced Strategy ---
    test_df['daily_return'] = test_df.groupby('Ticker')['Close'].pct_change()

    # --- NEW: Confidence-Weighted Portfolio Logic ---
    # We use the previous day's confidence scores as weights
    test_df['prev_confidence'] = test_df.groupby('Ticker')['confidence'].shift(1)
    
    # On each day, calculate the sum of confidence scores across all stocks
    total_daily_confidence = test_df.groupby('Date')['prev_confidence'].transform('sum')
    
    # The weight for each stock is its confidence divided by the total confidence for that day
    # This ensures our weights sum to 1 each day. We handle division by zero as well.
    test_df['portfolio_weight'] = test_df['prev_confidence'].div(total_daily_confidence).fillna(0)
    
    # The return for each stock on a given day is its daily return multiplied by its assigned weight
    test_df['strategy_return'] = test_df['daily_return'] * test_df['portfolio_weight']

    # --- Aggregate Portfolio Performance ---
    # The total portfolio return for a day is the sum of the weighted returns of all stocks
    portfolio_daily_returns = test_df.groupby('Date')['strategy_return'].sum()
    cumulative_returns = (1 + portfolio_daily_returns).cumprod()

    # --- Benchmark ---
    benchmark_daily_returns = test_df.groupby('Date')['daily_return'].mean()
    benchmark_cumulative_returns = (1 + benchmark_daily_returns).cumprod()
    
    # --- Metrics & Plotting ---
    print("\n--- Advanced Backtest Performance Metrics ---")
    total_return = (cumulative_returns.iloc[-1] - 1) * 100
    print(f"Total Strategy Return: {total_return:.2f}%")
    benchmark_total_return = (benchmark_cumulative_returns.iloc[-1] - 1) * 100
    print(f"Total Buy & Hold Return: {benchmark_total_return:.2f}%")
    sharpe_ratio = portfolio_daily_returns.mean() / portfolio_daily_returns.std() * np.sqrt(252)
    print(f"Strategy Sharpe Ratio: {sharpe_ratio:.2f}")

    print("\nGenerating performance plot...")
    plt.figure(figsize=(15, 7))
    (cumulative_returns * 100).plot(label='Advanced AI Strategy', legend=True)
    (benchmark_cumulative_returns * 100).plot(label='Buy and Hold Benchmark', legend=True)
    plt.title('Advanced Backtest: Confidence-Weighted Strategy vs. Buy & Hold')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value (Started at 100)')
    plt.grid(True)
    plt.savefig(plot_save_path)
    print(f"Plot saved to {plot_save_path}")
    plt.show()

if __name__ == "__main__":
    run_advanced_backtest(labeled_data_path=LABELED_DATA_PATH, model_path=MODEL_PATH, plot_save_path=PLOT_SAVE_PATH)