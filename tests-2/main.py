#Main file for the project: Stock Price Prediction using News Headlines
import os
import sys
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

# Function to fetch stock data
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
    plt.savefig(f"OUTPUTS\\{stock_ticker}_close_price.png")
    # plt.show()
    
def graph_stock_data_volume(stock_data,stock_ticker):
    plt.figure(figsize=(10, 5))
    plt.plot(stock_data.index, stock_data['Volume'], label=f"{stock_ticker} Stock Volume")
    plt.title(f"{stock_ticker} Stock Volume over Time")
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"OUTPUTS\\{stock_ticker}_volume.png")
    # plt.show()

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
    plt.savefig(f"OUTPUTS\\{stock_ticker}_high_low.png")
    # plt.show()
    
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

def predict_stock_trend(stock_ticker, stock_data, company_name, start_date, end_date, api_key, prediction_type):
    if stock_data is None or stock_data.empty:
        return None, None

    df = stock_data.copy()
    df['date'] = df.index.date
    df['return'] = df['Close'].pct_change()
    df['target'] = (df['return'].shift(-1) > 0).astype(int)
    # Technical indicators
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA10'] = df['Close'].rolling(window=10).mean()
    df['momentum'] = df['Close'].pct_change(5)
    df['volatility'] = df['Close'].rolling(window=5).std()
    df['trend_direction'] = np.where(df['MA5'] > df['MA10'], 1, 0)
    df.dropna(inplace=True)
    if len(df) < 5:
        print("Not enough data after applying indicators and cleaning. Please increase the number of days.")
        return None, None
    y = df['target']
    train_size = int(len(df) * 0.8)
    y_train = y.iloc[:train_size]
    if prediction_type == 1:
        # News only
        news_data = fetch_news_data(api_key, stock_data.index.date, company_name)
        df1 = process_data(stock_data, news_data)
        df1['news'] = news_data
        vectorizer = TfidfVectorizer(max_features=100)
        X_news = vectorizer.fit_transform(df1['news'].fillna('')).toarray()
        X_train = X_news[:train_size]
        model = train_model(X_train, y_train)
        latest_news = df1['news'].iloc[-1]
        latest_news_vec = vectorizer.transform([latest_news]).toarray()
        prediction = model.predict(latest_news_vec)
    elif prediction_type == 2:
        # Trends only
        X_tech = df[['momentum', 'volatility', 'trend_direction']].values
        X_train = X_tech[:train_size]
        model = train_model(X_train, y_train)
        latest_tech = df[['momentum', 'volatility', 'trend_direction']].iloc[-1:].values
        prediction = model.predict(latest_tech)
    else:
        # Combined
        news_data = fetch_news_data(api_key, stock_data.index.date, company_name)
        df1 = process_data(stock_data, news_data)
        df1['news'] = news_data
        vectorizer = TfidfVectorizer(max_features=100)
        X_news = vectorizer.fit_transform(df1['news'].fillna('')).toarray()
        X_tech = df[['momentum', 'volatility', 'trend_direction']].values
        X_combined = np.hstack((X_news, X_tech))
        X_train = X_combined[:train_size]
        model = train_model(X_train, y_train)
        latest_news = df1['news'].iloc[-1]
        latest_news_vec = vectorizer.transform([latest_news]).toarray()
        latest_tech = df[['momentum', 'volatility', 'trend_direction']].iloc[-1:].values
        latest_combined = np.hstack((latest_news_vec, latest_tech))
        prediction = model.predict(latest_combined)

    last_date = df['date'].iloc[-1]
    next_day = last_date + timedelta(days=1)
    return 'Up' if prediction[0] == 1 else 'Down', next_day

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
    plt.savefig(f"PREDICTED\\{stock_ticker}_prediction.png")
    plt.show()

def main():
    #Know The Stock
    # stock_ticker = input("Enter the stock ticker: ").upper()
    stock_ticker = "RS"
    # ndays = int(input("Enter number of days: "))
    ndays = 25

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
    predict_option = input("Do you want to predict the stock trend? (y/n): ").lower()
    
    if predict_option == 'y':
        print("\nPrediction Methods:")
        print("1. News headlines only")
        print("2. Previous price trends only")
        print("3. Combined (news + trends)")
        
        while True:
            try:
                prediction_type = int(input("\nSelect prediction method (1-3): "))
                if prediction_type not in [1, 2, 3]:
                    print("Please enter a number between 1 and 3.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
        
        # Only ask for company name if needed for news
        company_name = ""
        if prediction_type in [1, 3]:  # News only or Combined
            company_name = input("Enter the recognizable name of the company (e.g., 'Apple' for AAPL): ")
        
        api_key = os.getenv('NEWS_API_KEY', "c9c7b905272e46879386fb61ece03ab4")
        
        print("\nAnalyzing data and training prediction model...")
        trend, next_day = predict_stock_trend(stock_ticker,stock_data, company_name, start, end, api_key, prediction_type)
        
        if trend is None:
            print("Could not generate prediction. Not enough data available.")
        else:
            method_names = {1: "news headlines", 2: "price trends", 3: "combined analysis"}
            print(f"\nPredicted trend for {stock_ticker} on {next_day.strftime('%Y-%m-%d')}: {trend}")
            print(f"Prediction based on: {method_names[prediction_type]}")
            
            # Ensure PREDICTED directory exists
            if not os.path.exists("PREDICTED"):
                os.makedirs("PREDICTED")
                
            graph_prediction(stock_data, stock_ticker, trend, next_day)

if __name__ == "__main__":
    main()