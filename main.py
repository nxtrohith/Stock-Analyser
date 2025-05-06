#Main file for the project: Stock Price Prediction using News Headlines
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import datetime, timedelta ,date
from newsapi import NewsApiClient
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
        # Set a light background color for all pages
        plt.rcParams['figure.facecolor'] = '#f0f5f9'  # Light blue-gray background
        
        # Introduction page
        plt.figure(figsize=(10, 5))
        # Add a simple border/design element
        plt.axhline(y=0.8, color='#4a6fa5', linewidth=2)
        plt.axhline(y=0.2, color='#4a6fa5', linewidth=2)
        plt.text(0.5, 0.5, f"Stock Analysis Report\n\nStock Ticker: {stock_ticker}\nAnalysis Duration: Last {ndays} Days", 
                 fontsize=15, ha='center', va='center')
        plt.axis('off')  # Turn off the axis
        pdf.savefig()  # Save the introduction page
        plt.close()    # Close the figure

        # Calculate some basic statistics for the descriptive text
        avg_close = stock_data['Close'].mean()
        max_close = stock_data['Close'].max()
        min_close = stock_data['Close'].min()
        close_change = ((stock_data['Close'][-1] - stock_data['Close'][0]) / stock_data['Close'][0]) * 100
        avg_volume = stock_data['Volume'].mean()
        max_volume = stock_data['Volume'].max()
        
        # Create a page for each graph with descriptive text
        # Close Price Graph
        plt.figure(figsize=(10, 8))
        plt.subplot(5, 1, (1, 3))  # Use 3/5 of the space for the graph
        plt.plot(stock_data.index, stock_data['Close'], label=f"{stock_ticker} Stock Close Price")
        plt.title(f"{stock_ticker} Stock Price over Time")
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.xticks(rotation=45)
        
        # Add descriptive text below the graph
        plt.subplot(5, 1, (4, 5))  # Use 2/5 of the space for the text
        plt.axis('off')
        plt.text(0.05, 0.8, "Close Price Analysis:", fontsize=12, fontweight='bold')
        plt.text(0.05, 0.6, f"Average Price: ${avg_close:.2f}\nHighest Price: ${max_close:.2f}\nLowest Price: ${min_close:.2f}\nPrice Change: {close_change:.2f}%", 
                 fontsize=10, va='top', linespacing=1.5)
        plt.text(0.05, 0.2, "The closing price represents the final price at which a stock is traded on a given trading day. \nIt's a key indicator of market sentiment and is often used to track performance over time.", 
                 fontsize=9, va='top', linespacing=1.5, style='italic')
        
        plt.tight_layout()  # Adjust layout to prevent overlap
        pdf.savefig()  # Save the close price page
        plt.close()    # Close the figure
        
        # Volume Graph
        plt.figure(figsize=(10, 8))
        plt.subplot(5, 1, (1, 3))  # Use 3/5 of the space for the graph
        plt.plot(stock_data.index, stock_data['Volume'], label=f"{stock_ticker} Stock Volume", color='orange')
        plt.title(f"{stock_ticker} Stock Volume over Time")
        plt.xlabel('Date')
        plt.ylabel('Volume')
        plt.legend()
        plt.xticks(rotation=45)
        
        # Add descriptive text below the graph
        plt.subplot(5, 1, (4, 5))  # Use 2/5 of the space for the text
        plt.axis('off')
        plt.text(0.05, 0.8, "Volume Analysis:", fontsize=12, fontweight='bold')
        plt.text(0.05, 0.6, f"Average Daily Volume: {int(avg_volume):,} shares\nHighest Volume: {int(max_volume):,} shares", 
                 fontsize=10, va='top', linespacing=1.5)
        plt.text(0.05, 0.2, "Trading volume indicates the total number of shares traded during a given period. \nHigh volume often suggests strong interest in a stock and can validate price movements. \nUnusually high volume may indicate significant news or events affecting the stock.", 
                 fontsize=9, va='top', linespacing=1.5, style='italic')
        
        plt.tight_layout()  # Adjust layout to prevent overlap
        pdf.savefig()  # Save the volume page
        plt.close()    # Close the figure
        
        # High and Low Prices Graph
        plt.figure(figsize=(10, 8))
        plt.subplot(5, 1, (1, 3))  # Use 3/5 of the space for the graph
        plt.plot(stock_data.index, stock_data['High'], label=f"{stock_ticker} Stock High Price", color='green')
        plt.plot(stock_data.index, stock_data['Low'], label=f"{stock_ticker} Stock Low Price", color='red')
        plt.title(f"{stock_ticker} Stock High and Low Price over Time")
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.xticks(rotation=45)
        
        # Add descriptive text below the graph
        plt.subplot(5, 1, (4, 5))  # Use 2/5 of the space for the text
        plt.axis('off')
        plt.text(0.05, 0.8, "High/Low Price Analysis:", fontsize=12, fontweight='bold')
        plt.text(0.05, 0.6, f"Average High: ${stock_data['High'].mean():.2f}\nAverage Low: ${stock_data['Low'].mean():.2f}\nHighest Price: ${stock_data['High'].max():.2f}\nLowest Price: ${stock_data['Low'].min():.2f}", 
                 fontsize=10, va='top', linespacing=1.5)
        plt.text(0.05, 0.2, "The high and low prices show the range in which a stock traded during each day. \nWider ranges between high and low prices indicate higher volatility. \nConsistent patterns in these ranges can help identify support and resistance levels.", 
                 fontsize=9, va='top', linespacing=1.5, style='italic')
        
        plt.tight_layout()  # Adjust layout to prevent overlap
        pdf.savefig()  # Save the high/low page
        plt.close()    # Close the figure
        
        # Reset the background color to default
        plt.rcParams['figure.facecolor'] = 'white'

        plt.tight_layout()
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