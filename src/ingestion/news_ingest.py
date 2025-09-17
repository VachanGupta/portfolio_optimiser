import os
import json
from pathlib import Path
from newsapi import NewsApiClient
from dotenv import load_dotenv
from datetime import datetime, timedelta # Import datetime libraries

# --- Configuration ---
load_dotenv()

SEARCH_QUERIES = {
    'RELIANCE.NS': 'Reliance Industries',
    'TCS.NS': 'Tata Consultancy Services',
    'HDFCBANK.NS': 'HDFC Bank',
    'INFY.NS': 'Infosys',
    'ICICIBANK.NS': 'ICICI Bank'
}

# --- FIX: Automatically calculate the start date to be 29 days ago ---
# This ensures we are always within the free plan's 1-month limit.
START_DATE = (datetime.today() - timedelta(days=29)).strftime('%Y-%m-%d')
END_DATE = datetime.today().strftime('%Y-%m-%d') 

SAVE_DIR = Path(__file__).parent.parent.parent / "data/raw/news"


def fetch_news(api_key, queries, start_date, end_date, save_dir):
    """
    Fetches news articles for a list of queries from NewsAPI and saves them as JSON files.
    """
    if not api_key:
        print("Error: NEWSAPI_KEY not found. Please add it to your .env file.")
        return
        
    newsapi = NewsApiClient(api_key=api_key)
    save_dir.mkdir(parents=True, exist_ok=True)
    
    for ticker, query in queries.items():
        print(f"Fetching news for {query} ({ticker})...")
        try:
            all_articles = newsapi.get_everything(q=query,
                                                  from_param=start_date,
                                                  to=end_date,
                                                  language='en',
                                                  sort_by='publishedAt')
            
            file_path = save_dir / f"{ticker}_news.json"
            with open(file_path, 'w') as f:
                json.dump(all_articles, f, indent=4)
                
            print(f"Successfully fetched {all_articles['totalResults']} articles and saved to {file_path}")
        
        except Exception as e:
            print(f"An error occurred for query '{query}': {e}")


if __name__ == "__main__":
    api_key = os.getenv("NEWSAPI_KEY")
    fetch_news(api_key=api_key, 
               queries=SEARCH_QUERIES,
               start_date=START_DATE,
               end_date=END_DATE,
               save_dir=SAVE_DIR)