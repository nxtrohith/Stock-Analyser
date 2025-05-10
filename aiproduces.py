#Main file for the project: Stock Price Prediction using News Headlines
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import datetime, timedelta ,date
from newsapi import NewsApiClient
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def fetch_stock_data(stock_ticker, start_date, end_date):
    try:
        stock_data = yf.download(stock_ticker, start=start_date, end=end_date)
        if stock_data.empty:
            print("No data available for the given date range.")
            return None
        return stock_data
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None

def graph_stock_data_close(stock_data,stock_ticker):
    plt.figure(figsize=(10, 5))
    plt.plot(stock_data.index, stock_data['Close'], label=f"{stock_ticker} Stock Close Price")
    plt.title(f"{stock_ticker} Stock Price over Time")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{stock_ticker}_close_price.png")
    plt.show()
    
def graph_stock_data_volume(stock_data,stock_ticker):
    plt.figure(figsize=(10, 5))
    plt.plot(stock_data.index, stock_data['Volume'], label=f"{stock_ticker} Stock Volume")
    plt.title(f"{stock_ticker} Stock Volume over Time")
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{stock_ticker}_volume.png")
    plt.show()

def graph_stock_data_high_low(stock_data,stock_ticker):
    plt.figure(figsize=(10, 5))
    plt.plot(stock_data.index, stock_data['High'], label=f"{stock_ticker} Stock High Price")
    plt.plot(stock_data.index, stock_data['Low'], label=f"{stock_ticker} Stock Low Price")
    plt.title(f"{stock_ticker} Stock High and Low Price over Time")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{stock_ticker}_high_low.png")
    plt.show()
    
def fetch_news_data(api_key, dates, company_name):
    """Fetch news headlines for each date."""
    newsapi = NewsApiClient(api_key=api_key)
    news_data = []
    for date in dates:
        articles = newsapi.get_everything(q=company_name, from_param=str(date), to=str(date), language='en', sort_by="publishedAt")
        headlines = [article['title'] for article in articles['articles']]
        news_data.append(' '.join(headlines))
    return news_data

def process_data(stock_data, news_data):
    """Process stock and news data to create features and target variable."""
    df = stock_data.copy()
    df['date'] = df.index.date
    df['news'] = news_data
    df['return'] = df['Close'].pct_change()
    df['target'] = (df['return'].shift(-1) > 0).astype(int)
    df.dropna(inplace=True)
    return df

def train_model(X_train, y_train):
    """Train the logistic regression model."""
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model

def predict_trend(model, latest_news, vectorizer, last_date):
    """Predict the trend based on the latest news and return the date of the prediction."""
    latest_news_vec = vectorizer.transform([latest_news]).toarray()
    prediction = model.predict(latest_news_vec)
    # Calculate the next day's date
    next_day = last_date + timedelta(days=1)
    return 'Up' if prediction[0] == 1 else 'Down', next_day

def predict_stock_trend(stock_ticker, company_name, start_date, end_date, api_key):
    """Predict the stock trend based on news headlines."""
    # Fetch data
    stock_data = fetch_stock_data(stock_ticker, start_date, end_date)
    
    if stock_data is None or stock_data.empty:
        return None, None
    
    news_data = fetch_news_data(api_key, stock_data.index.date, company_name)
    
    # Process data
    df = process_data(stock_data, news_data)
    
    if df.empty or len(df) < 5:  # Need enough data to train
        return None, None
    
    # Feature extraction
    vectorizer = TfidfVectorizer(max_features=100)
    X_news = vectorizer.fit_transform(df['news'].fillna('')).toarray()
    y = df['target']
    
    # Train/test split
    train_size = int(len(df) * 0.8)
    X_train = X_news[:train_size]
    y_train = y.iloc[:train_size]
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Predict for the latest news
    latest_news = df['news'].iloc[-1]
    last_date = df['date'].iloc[-1]
    trend, next_day = predict_trend(model, latest_news, vectorizer, last_date)
    
    return trend, next_day

def graph_prediction(stock_data, stock_ticker, trend, prediction_date):
    """Create a graph showing historical data and prediction."""
    plt.figure(figsize=(12, 6))
    
    # Plot historical close prices
    plt.plot(stock_data.index, stock_data['Close'], label=f"{stock_ticker} Historical Close Price", color='blue')
    
    # Get the last close price
    last_close = stock_data['Close'].iloc[-1]
    
    # Plot the prediction point
    if trend == 'Up':
        marker_color = 'green'
        predicted_price = last_close * 1.01  # Just for visualization, assume 1% increase
    else:
        marker_color = 'red'
        predicted_price = last_close * 0.99  # Just for visualization, assume 1% decrease
    
    # Add prediction marker
    plt.scatter([prediction_date], [predicted_price], color=marker_color, s=100, zorder=5)
    
    # Add an arrow and annotation for the prediction
    plt.annotate(f"Predicted: {trend}",
                xy=(prediction_date, predicted_price),
                xytext=(prediction_date - timedelta(days=2), predicted_price * 1.05 if trend == 'Up' else predicted_price * 0.95),
                arrowprops=dict(facecolor=marker_color, shrink=0.05),
                fontsize=10,
                color=marker_color)
    
    plt.title(f"{stock_ticker} Stock Price with Prediction for {prediction_date.strftime('%Y-%m-%d')}")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{stock_ticker}_prediction.png")
    plt.show()

def main():
    #Know The Stock
    stock_ticker = input("Enter the stock ticker: ").upper()
    ndays = int(input("Enter number of days: "))

    start = (date.today() - timedelta(days=ndays+4)).strftime("%Y-%m-%d")
    end = (date.today() - timedelta(days=3)).strftime("%Y-%m-%d")

    # Fetch the stock data
    stock_data = fetch_stock_data(stock_ticker, start, end)
    
    if stock_data is None:
        print("No data available for the given stock ticker.")
        print("Please make sure you have entered the correct stock ticker.")
        return
    
    print(stock_data)

    #Generate the graphs
    graph_stock_data_close(stock_data, stock_ticker)
    graph_stock_data_volume(stock_data, stock_ticker)
    graph_stock_data_high_low(stock_data, stock_ticker)
    
    # Ask if user wants to predict trend
    predict_option = input("Do you want to predict the stock trend based on news? (y/n): ").lower()
    
    if predict_option == 'y':
        company_name = input("Enter the recognizable name of the company (e.g., 'Apple' for AAPL): ")
        api_key = '7c1c81c5012c432c8114f0cbe4b9b221'  # Your NewsAPI key
        
        print("Fetching news and training prediction model...")
        trend, next_day = predict_stock_trend(stock_ticker, company_name, start, end, api_key)
        
        if trend is None:
            print("Could not generate prediction. Not enough news data available.")
        else:
            print(f"Predicted trend for {stock_ticker} on {next_day.strftime('%Y-%m-%d')}: {trend}")
            graph_prediction(stock_data, stock_ticker, trend, next_day)

if __name__ == "__main__":
    main()