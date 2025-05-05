#Main file for the project: Stock Price Prediction using News Headlines

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import datetime, timedelta ,date
from newsapi import NewsApiClient
from fpdf import FPDF
from matplotlib.backends.backend_pdf import PdfPages

def fetch_stock_data(stock_ticker, start_date, end_date):
    try:
        stock_data = yf.download(stock_ticker, start=start_date, end=end_date)
        return stock_data
    except AttributeError as e:
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
    
def generate_pdf_report(stock_data, stock_ticker, ndays):
    with PdfPages(f"{stock_ticker}_report.pdf") as pdf:
        # Introduction page
        plt.figure(figsize=(10, 5))
        plt.text(0.5, 0.5, f"Stock Analysis Report\n\nStock Ticker: {stock_ticker}\nAnalysis Duration: Last {ndays} Days", 
                 fontsize=15, ha='center', va='center')
        plt.axis('off')  # Turn off the axis
        pdf.savefig()  # Save the introduction page
        plt.close()    # Close the figure

        # Create a new page for the graphs
        plt.figure(figsize=(10, 15))

        # Graph for Close Price
        plt.subplot(3, 1, 1)  # 3 rows, 1 column, 1st subplot
        plt.plot(stock_data.index, stock_data['Close'], label=f"{stock_ticker} Stock Close Price")
        plt.title(f"{stock_ticker} Stock Price over Time")
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.xticks(rotation=45)

        # Graph for Volume
        plt.subplot(3, 1, 2)  # 3 rows, 1 column, 2nd subplot
        plt.plot(stock_data.index, stock_data['Volume'], label=f"{stock_ticker} Stock Volume", color='orange')
        plt.title(f"{stock_ticker} Stock Volume over Time")
        plt.xlabel('Date')
        plt.ylabel('Volume')
        plt.legend()
        plt.xticks(rotation=45)

        # Graph for High and Low Prices
        plt.subplot(3, 1, 3)  # 3 rows, 1 column, 3rd subplot
        plt.plot(stock_data.index, stock_data['High'], label=f"{stock_ticker} Stock High Price", color='green')
        plt.plot(stock_data.index, stock_data['Low'], label=f"{stock_ticker} Stock Low Price", color='red')
        plt.title(f"{stock_ticker} Stock High and Low Price over Time")
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.xticks(rotation=45)

        plt.tight_layout()  # Adjust layout to prevent overlap
        pdf.savefig()  # Save the graphs page
        plt.close()    # Close the figure

def main():
    #Know The Stock
    stock_ticker = input("Enter the stock ticker: ").upper()
    ndays = int(input("Enter number of days: "))

    start = (date.today() - timedelta(days=ndays+4)).strftime("%Y-%m-%d")
    end = (date.today() - timedelta(days=3)).strftime("%Y-%m-%d")

    # Fetch the stock data
    stock_data = fetch_stock_data(stock_ticker, start, end)
    print(stock_data)

    #Generate the graphs
    graph_stock_data_close(stock_data,stock_ticker)
    graph_stock_data_volume(stock_data,stock_ticker)
    graph_stock_data_high_low(stock_data,stock_ticker)
    
    #Generate the PDF report
    generate_pdf_report(stock_data, stock_ticker, ndays)


if __name__ == "__main__":
    main()