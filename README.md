# portfolio_optimiser


<!-- source .venv/bin/activate -->

# 🤖 Intelligent Stock Portfolio Optimizer

An end-to-end machine learning system that forecasts short-term stock returns for a portfolio of Indian equities and demonstrates a full MLOps lifecycle from data ingestion to containerized deployment.

---

## 🌟 Key Features

* **End-to-End Pipeline:** Automates the entire process from raw data collection to a final, interactive user dashboard.
* **Hybrid Feature Engineering:** Combines traditional quantitative features (**Technical Indicators**) with modern NLP-based features (**News Sentiment Analysis** using FinBERT).
* **Rigorous Backtesting:** Implements a realistic backtest simulation that accounts for **transaction costs** to validate strategy performance against a benchmark.
* **Model Explainability:** Uses **SHAP (SHapley Additive exPlanations)** to interpret the model's predictions and identify the most influential features.
* **API-First Architecture:** Built with a decoupled backend (**FastAPI**) that serves the model's predictions, and a separate frontend (**Streamlit**) that consumes the API.
* **Containerized Deployment:** The entire multi-service application is containerized using **Docker** and managed with **Docker Compose** for easy, reproducible deployment.

---

## 🏗️ Architecture

The project follows a modern, multi-service architecture:

```
+----------------+      +-------------------+      +-----------------+      +--------------------+      +----------------+
|  Data Sources  |----->|  Python Scripts   |----->|   Saved Model   |----->|  FastAPI Backend   |----->| Streamlit      |
| (yfinance,     |      |  (Data Ingestion, |      |  (xgb_model.    |      |  (Loads model,     |      |  Frontend      |
|  NewsAPI)      |      |   Feature Eng.)   |      |   joblib)       |      |   serves preds)    |      |  (Calls API,   |
+----------------+      +-------------------+      +-----------------+      +--------------------+      |   visualizes)  |
                                                                             (Container 1)             (Container 2)
```

---

## 🛠️ Tech Stack

* **Backend:** FastAPI, Uvicorn
* **Frontend:** Streamlit
* **Data Science:** Pandas, NumPy, Scikit-learn, XGBoost
* **NLP:** Transformers (Hugging Face), FinBERT
* **Quantitative Finance:** PyPortfolioOpt, pandas-ta, SHAP
* **MLOps & Deployment:** Docker, Docker Compose
* **Data Ingestion:** yfinance, NewsAPI-Python

---

## 🖼️ Screenshots

### Streamlit Dashboard
*(Here, you should insert a screenshot of your running Streamlit application)*
`![Dashboard Screenshot](path/to/your/dashboard_screenshot.png)`

### Advanced Backtest Performance
*(Here, you should insert your `advanced_backtest_performance.png` chart)*
`![Backtest Screenshot](advanced_backtest_performance.png)`

### Feature Importance (SHAP)
*(Here, you should insert your `feature_importance.png` chart)*
`![SHAP Screenshot](feature_importance.png)`


---

## 🚀 Setup and Usage

This project is fully containerized, making setup incredibly simple.

### Prerequisites
* [Docker](https://www.docker.com/products/docker-desktop/) installed and running.
* A NewsAPI key.

### Installation & Running
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/portfolio-optimizer.git](https://github.com/your-username/portfolio-optimizer.git)
    cd portfolio-optimizer
    ```
2.  **Set up your API Key:**
    Create a `.env` file from the template and add your secret key.
    ```bash
    cp .env.example .env
    # Now, edit the .env file with your NewsAPI key
    ```
3.  **Build and run with Docker Compose:**
    This single command will build the images and start both the API and the dashboard services.
    ```bash
    docker-compose up --build
    ```
4.  **Access the Dashboard:**
    Open your web browser and navigate to **`http://localhost:8502`**.

---

## 📂 File Structure

* **`/app`**: Contains the Streamlit frontend code (`dashboard.py`).
* **`/data`**: Stores raw, processed, and final labeled data.
* **`/models`**: Stores the saved model (`.joblib`) and model explanation scripts.
* **`/src`**: Contains all the core Python modules for data ingestion, feature engineering, and the API backend.
* **`Dockerfile`**: Instructions to build the application container.
* **`docker-compose.yml`**: Defines and orchestrates the multi-service application.

---

## ⚠️ Disclaimer
This project is for educational and demonstrational purposes only. It is not financial advice. All investment decisions carry risk, and you should consult a qualified professional before making any.
