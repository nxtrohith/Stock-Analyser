#Main file for the project: Stock Price Prediction using News Headlines

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import datetime, timedelta
from newsapi import NewsApiClient

def fetch_stock_data(stock_ticker, start_date, end_date):
    stock_data = yf.download(stock_ticker, start=start_date, end=end_date)
    return stock_data

def graph_stock_data_close(stock_data,stock_ticker):
    plt.figure(figsize=(20, 10))
    plt.plot(stock_data.index, stock_data['Close'], label=f"{stock_ticker} Stock Close Price")
    plt.title(f"{stock_ticker} Stock Price over Time")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
def graph_stock_data_volume(stock_data,stock_ticker):
    plt.figure(figsize=(20, 10))
    plt.plot(stock_data.index, stock_data['Volume'], label=f"{stock_ticker} Stock Volume")
    plt.title(f"{stock_ticker} Stock Volume over Time")
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def graph_stock_data_high_low(stock_data,stock_ticker):
    plt.figure(figsize=(20, 10))
    plt.plot(stock_data.index, stock_data['High'], label=f"{stock_ticker} Stock High Price")
    plt.plot(stock_data.index, stock_data['Low'], label=f"{stock_ticker} Stock Low Price")
    plt.title(f"{stock_ticker} Stock High and Low Price over Time")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
def main():
    #Know The Stock
    stock_ticker = input("Enter the stock ticker: ")
    start_date = input("Enter the start date: ")
    end_date = input("Enter the end date: ")
    # Fetch the stock data
    stock_data = fetch_stock_data(stock_ticker, start_date, end_date)
    print(stock_data,stock_ticker)


if __name__ == "__main__":
    main()