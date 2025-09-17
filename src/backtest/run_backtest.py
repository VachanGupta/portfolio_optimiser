import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import matplotlib.pyplot as plt

# --- File Paths ---
LABELED_DATA_PATH = Path(__file__).parent.parent.parent / "data/processed/labeled_features.csv"
MODEL_PATH = Path(__file__).parent.parent.parent / "models/xgb_model.joblib"
PLOT_SAVE_PATH = Path(__file__).parent.parent.parent / "backtest_performance_with_costs.png"

# --- NEW: Configuration for Transaction Costs ---
TRANSACTION_COST_BPS = 10 # Basis points, e.g., 10 bps = 0.1%

def run_backtest(labeled_data_path, model_path, plot_save_path):
    """
    Runs a backtest simulation including transaction costs.
    """
    print("Loading model and data for backtest...")
    model = joblib.load(model_path)
    df = pd.read_csv(labeled_data_path, parse_dates=['Date'])
    
    test_df = df[df['Date'] >= '2025-01-01'].copy()
    
    features_to_drop = ['Date', 'Ticker', 'future_return', 'target', 
                        'Open', 'High', 'Low', 'Adj Close', 'Volume']
    X_test = test_df.drop(columns=features_to_drop)
    
    print("Generating predictions for the test period...")
    test_df['prediction'] = model.predict(X_test)
    
    # --- Simulate Strategy ---
    test_df['daily_return'] = test_df.groupby('Ticker')['Close'].pct_change()
    
    # --- NEW: Logic to include transaction costs ---
    # A "trade" happens when our prediction signal changes from the previous day (e.g., from 0 to 1 or 1 to 0)
    test_df['prev_prediction'] = test_df.groupby('Ticker')['prediction'].shift(1)
    test_df['trade'] = (test_df['prediction'] != test_df['prev_prediction']).astype(int)
    
    # Calculate strategy returns, then subtract costs on days we trade
    test_df['strategy_return'] = test_df['daily_return'] * test_df['prev_prediction'] # Use previous day's signal
    test_df['strategy_return'] -= test_df['trade'] * (TRANSACTION_COST_BPS / 10000)
    
    # --- Aggregate Portfolio Performance ---
    portfolio_daily_returns = test_df.groupby('Date')['strategy_return'].mean()
    cumulative_returns = (1 + portfolio_daily_returns).cumprod()
    
    # --- Calculate Benchmark (Buy and Hold) ---
    benchmark_daily_returns = test_df.groupby('Date')['daily_return'].mean()
    benchmark_cumulative_returns = (1 + benchmark_daily_returns).cumprod()
    
    # --- Performance Metrics ---
    print("\n--- Backtest Performance Metrics (with Transaction Costs) ---")
    total_return = (cumulative_returns.iloc[-1] - 1) * 100
    print(f"Total Strategy Return: {total_return:.2f}%")
    benchmark_total_return = (benchmark_cumulative_returns.iloc[-1] - 1) * 100
    print(f"Total Buy & Hold Return: {benchmark_total_return:.2f}%")
    sharpe_ratio = portfolio_daily_returns.mean() / portfolio_daily_returns.std() * np.sqrt(252)
    print(f"Strategy Sharpe Ratio: {sharpe_ratio:.2f}")

    # --- Plotting ---
    print("\nGenerating performance plot...")
    plt.figure(figsize=(15, 7))
    (cumulative_returns * 100).plot(label='AI Strategy (with Costs)', legend=True)
    (benchmark_cumulative_returns * 100).plot(label='Buy and Hold Benchmark', legend=True)
    plt.title('Backtest Performance: AI Strategy vs. Buy & Hold')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value (Started at 100)')
    plt.grid(True)
    plt.savefig(plot_save_path)
    print(f"Plot saved to {plot_save_path}")
    plt.show()

if __name__ == "__main__":
    run_backtest(labeled_data_path=LABELED_DATA_PATH, model_path=MODEL_PATH, plot_save_path=PLOT_SAVE_PATH)