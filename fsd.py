import yfinance as yf
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from newsapi import NewsApiClient
from datetime import timedelta

def fetch_stock_data(ticker, start_date, end_date):
    """Fetch historical stock data."""
    data = yf.download(ticker, start=start_date, end=end_date)
    print(data)
    return data

def fetch_news_data(api_key, dates, mncname):
    """Fetch news headlines for each date."""
    newsapi = NewsApiClient(api_key=api_key)
    news_data = []
    for date in dates:
        articles = newsapi.get_everything(q=mncname, from_param=str(date), to=str(date), language='en', sort_by="publishedAt")
        headlines = [article['title'] for article in articles['articles']]
        news_data.append(' '.join(headlines))
        # print()
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

def main():
    # Parameters
    ticker = input("Enter the ticker:")
    start_date = input("Enter the start date:")
    end_date = input("Enter the end date:")
    mncname = input("Enter the Recognisable name of the company:")
    api_key = '7c1c81c5012c432c8114f0cbe4b9b221'

    # Fetch data
    stock_data = fetch_stock_data(ticker, start_date, end_date)
    news_data = fetch_news_data(api_key, stock_data.index.date, mncname)

    # Process data
    df = process_data(stock_data, news_data)
    print(df['news'])

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
    last_date = df['date'].iloc[-1]  # Get the last date from the DataFrame
    trend, next_day = predict_trend(model, latest_news, vectorizer, last_date)
    print(f'Predicted trend for {mncname} based on news: {trend}')

if __name__ == "__main__":
    main()