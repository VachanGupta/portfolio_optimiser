import pandas as pd
import json
from pathlib import Path
from transformers import pipeline
import time

# --- File Paths ---
NEWS_DATA_DIR = Path(__file__).parent.parent.parent / "data/raw/news"
FEATURES_PATH = Path(__file__).parent.parent.parent / "data/processed/sentiment_features.csv"

# Define the tickers we're processing
TICKERS = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS']

def generate_sentiment_scores(news_dir, tickers, features_path):
    """
    Loads raw news data from JSON files, runs sentiment analysis on headlines,
    aggregates a daily sentiment score, and saves the result to a CSV file.
    """
    print("Loading FinBERT sentiment analysis model...")
    # This will download the model from Hugging Face the first time it's run
    sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")
    
    all_sentiments = []

    for ticker in tickers:
        news_file = news_dir / f"{ticker}_news.json"
        if not news_file.exists():
            print(f"News file for {ticker} not found. Skipping.")
            continue
            
        print(f"Processing sentiment for {ticker}...")
        with open(news_file, 'r') as f:
            news_data = json.load(f)
        
        articles = news_data.get('articles', [])
        if not articles:
            print(f"No articles found for {ticker}. Skipping.")
            continue
        
        # Prepare data for the pipeline
        headlines = [article['title'] for article in articles if article['title']]
        publish_dates = [article['publishedAt'] for article in articles if article['title']]
        
        # Run sentiment analysis in batches for efficiency
        sentiment_results = sentiment_pipeline(headlines)
        
        # Process results
        # Convert labels to numerical values: positive=1, neutral=0, negative=-1
        score_map = {'positive': 1, 'neutral': 0, 'negative': -1}
        
        processed_articles = []
        for i, result in enumerate(sentiment_results):
            numeric_sentiment = score_map[result['label']] * result['score']
            processed_articles.append({
                'publishedAt': publish_dates[i],
                'sentiment_score': numeric_sentiment
            })
        
        if not processed_articles:
            print(f"No valid articles to process for {ticker}. Skipping.")
            continue

        # Create a DataFrame and aggregate scores by day
        sentiment_df = pd.DataFrame(processed_articles)
        sentiment_df['Date'] = pd.to_datetime(sentiment_df['publishedAt']).dt.date
        daily_sentiment = sentiment_df.groupby('Date')['sentiment_score'].mean().reset_index()
        daily_sentiment['Ticker'] = ticker
        
        all_sentiments.append(daily_sentiment)
        print(f"Finished processing {len(headlines)} headlines for {ticker}.")

    if not all_sentiments:
        print("No sentiment data was generated. Exiting.")
        return

    # Combine all tickers into a single DataFrame and save
    final_df = pd.concat(all_sentiments)
    final_df['Date'] = pd.to_datetime(final_df['Date']) # Ensure Date is datetime object
    
    features_path.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(features_path, index=False)
    
    print(f"\nSentiment features saved successfully to {features_path}!")
    print("--- Sample of generated sentiment features: ---")
    print(final_df.head())


if __name__ == "__main__":
    generate_sentiment_scores(news_dir=NEWS_DATA_DIR, tickers=TICKERS, features_path=FEATURES_PATH)