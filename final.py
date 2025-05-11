#Main file for the project: Stock Price Prediction using News Headlines
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from pandas.core.groupby.groupby import base
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

class GraPhs:
    def __init__(self, base_graphs_path, gshow=False):
        self.base_graphs_path = base_graphs_path
        self.gshow = gshow

    def stock_data_close(self, stock_data, stock_ticker):
        plt.figure(figsize=(10, 5))
        plt.plot(stock_data.index, stock_data['Close'], label=f"{stock_ticker} Stock Close Price")
        plt.title(f"{stock_ticker} Stock Price over Time")
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{self.base_graphs_path}\\{stock_ticker}_close_price.png")
        if self.gshow:
            plt.show()

    def stock_data_volume(self, stock_data, stock_ticker):
        plt.figure(figsize=(10, 5))
        plt.plot(stock_data.index, stock_data['Volume'], label=f"{stock_ticker} Stock Volume")
        plt.title(f"{stock_ticker} Stock Volume over Time")
        plt.xlabel('Date')
        plt.ylabel('Volume')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{self.base_graphs_path}\\{stock_ticker}_volume.png")
        if self.gshow:
            plt.show()

    def stock_data_high_low(self, stock_data, stock_ticker):
        plt.figure(figsize=(10, 5))
        plt.plot(stock_data.index, stock_data['High'], label=f"{stock_ticker} Stock High Price")
        plt.plot(stock_data.index, stock_data['Low'], label=f"{stock_ticker} Stock Low Price")
        plt.title(f"{stock_ticker} Stock High and Low Price over Time")
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{self.base_graphs_path}\\{stock_ticker}_high_low.png")
        if self.gshow:
            plt.show()

    def prediction(self, stock_data, stock_ticker, trend, prediction_date):
        plt.figure(figsize=(14,7))
        plt.plot(stock_data.index, stock_data['Close'], label=f"{stock_ticker} Historical Close Price", color='blue')
        last_close = stock_data['Close'].iloc[-1]
        if trend == 'Up':
            marker_color = 'green'
            predicted_price = last_close * 1.01
        else:
            marker_color = 'red'
            predicted_price = last_close * 0.99
        plt.scatter([prediction_date], [predicted_price], color=marker_color, s=100, zorder=5)
        plt.annotate(f"Predicted: {trend}",
                    xy=(prediction_date, predicted_price),
                    xytext=(prediction_date - timedelta(days=2), predicted_price * 1.05 if trend == 'Up' else predicted_price * 0.95),
                    arrowprops=dict(facecolor=marker_color, shrink=0.001),
                    fontsize=12,
                    color=marker_color)
        plt.title(f"{stock_ticker} Stock Price with Prediction for {prediction_date.strftime('%Y-%m-%d')}")
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        # plt.tight_layout()
        plt.savefig(f"{predicted_graphs_path}\\{stock_ticker}_prediction.png")
        plt.show()


class StockPredictor:
    def __init__(self, stock_ticker, start_date, end_date, api_key, company_name=None):
        self.stock_ticker = stock_ticker
        self.start_date = start_date
        self.end_date = end_date
        self.api_key = api_key
        self.company_name = company_name
        self.stock_data = None
        self.news_data = None
        self.df = None
        self.vectorizer = None
        self.model = None

    def fetch_data(self):
        self.stock_data = fetch_stock_data(self.stock_ticker, self.start_date, self.end_date)
        if self.stock_data is None or self.stock_data.empty:
            return False
        if self.api_key and self.company_name:
            self.news_data = fetch_news_data(self.api_key, self.stock_data.index.date, self.company_name)
        else:
            self.news_data = [''] * len(self.stock_data)
        self.df = process_data(self.stock_data, self.news_data)
        if self.df.empty or len(self.df) < 10:
            return False
        # Add technical indicators
        self.df['MA5'] = self.df['Close'].rolling(window=5).mean()
        self.df['MA10'] = self.df['Close'].rolling(window=10).mean()
        self.df['momentum'] = self.df['Close'].pct_change(5)
        self.df['volatility'] = self.df['Close'].rolling(window=5).std()
        self.df['trend_direction'] = np.where(self.df['MA5'] > self.df['MA10'], 1, 0)
        self.df.dropna(inplace=True)
        return len(self.df) >= 5

    def predict(self, prediction_type=3):
        if self.df is None or len(self.df) < 5:
            return None, None
        y = self.df['target']
        train_size = int(len(self.df) * 0.8)
        y_train = y.iloc[:train_size]
        if prediction_type == 1:
            # Trends only
            X_tech = self.df[['momentum', 'volatility', 'trend_direction']].values
            X_train = X_tech[:train_size]
            self.model = train_model(X_train, y_train)
            latest_tech = self.df[['momentum', 'volatility', 'trend_direction']].iloc[-1:].values
            prediction = self.model.predict(latest_tech)
        elif prediction_type == 2:
            # News only
            self.vectorizer = TfidfVectorizer(max_features=100)
            X_news = self.vectorizer.fit_transform(self.df['news'].fillna('')).toarray()
            X_train = X_news[:train_size]
            self.model = train_model(X_train, y_train)
            latest_news = self.df['news'].iloc[-1]
            latest_news_vec = self.vectorizer.transform([latest_news]).toarray()
            prediction = self.model.predict(latest_news_vec)
        else:
            # Combined
            self.vectorizer = TfidfVectorizer(max_features=100)
            X_news = self.vectorizer.fit_transform(self.df['news'].fillna('')).toarray()
            X_tech = self.df[['momentum', 'volatility', 'trend_direction']].values
            X_combined = np.hstack((X_news, X_tech))
            X_train = X_combined[:train_size]
            self.model = train_model(X_train, y_train)
            latest_news = self.df['news'].iloc[-1]
            latest_news_vec = self.vectorizer.transform([latest_news]).toarray()
            latest_tech = self.df[['momentum', 'volatility', 'trend_direction']].iloc[-1:].values
            latest_combined = np.hstack((latest_news_vec, latest_tech))
            prediction = self.model.predict(latest_combined)
            last_date = pd.to_datetime(self.df['date'].iloc[-1]).date()
        next_day = last_date

        return 'Up' if prediction[0] == 1 else 'Down', next_day

def main():
    # Know The Stock
    api_key = 'c9c7b905272e46879386fb61ece03ab4'  # Your NewsAPI key
    stock_ticker = input("Enter the stock ticker: ").upper()
    ndays = int(input("Enter number of days: "))
    start = (date.today() - timedelta(days=ndays+4)).strftime("%Y-%m-%d")
    end = (date.today() - timedelta(days=3)).strftime("%Y-%m-%d")
    stock_data = fetch_stock_data(stock_ticker, start, end)
    if stock_data is None:
        print("No data available for the given stock ticker.")
        print("Please make sure you have entered the correct stock ticker.")
        return
    print(stock_data)
    graphs = GraPhs(base_graphs_path, gshow)
    graphs.stock_data_close(stock_data, stock_ticker)
    graphs.stock_data_volume(stock_data, stock_ticker)
    graphs.stock_data_high_low(stock_data, stock_ticker)
    predict_option = input("Do you want to predict the stock trend? (y/n): ").lower()
    if predict_option == 'y':
        print("Select prediction method:")
        print("1. Based on recent trends")
        print("2. Based on recent news")
        print("3. Combination of both")
        while True:
            try:
                prediction_type = int(input("Enter 1, 2, or 3: "))
                if prediction_type in [1, 2, 3]:
                    break
                else:
                    print("Please enter 1, 2, or 3.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        company_name = None
        # api_key = None
        if prediction_type in [2, 3]:
            company_name = input("Enter the recognizable name of the company (e.g., 'Apple' for AAPL): ")
        predictor = StockPredictor(stock_ticker, start, end, api_key, company_name)
        print("Fetching data and training prediction model...")
        if predictor.fetch_data():
            trend, next_day = predictor.predict(prediction_type=prediction_type)
            if trend is None:
                print("Could not generate prediction. Not enough data available.")
            else:
                print(f"Predicted trend for {stock_ticker} on {next_day.strftime('%Y-%m-%d')}: {trend}")
                graphs.prediction(stock_data, stock_ticker, trend, next_day)
        else:
            print("Could not generate prediction. Not enough data available.")

if not os.path.exists("OUTPUTS"):
    os.makedirs("OUTPUTS")
if not os.path.exists("PREDICTED"):
    os.makedirs("PREDICTED")
# Path to save the base graphs
base_graphs_path = "OUTPUTS"
predicted_graphs_path = "PREDICTED"

# Indicates whether to show the graphs or not
gshow = False

if __name__ == "__main__":
    main()