#Main file for the project: Stock Price Prediction using News Headlines

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import datetime, timedelta ,date
from newsapi import NewsApiClient
from fpdf import FPDF

def fetch_stock_data(stock_ticker, start_date, end_date):
    stock_data = yf.download(stock_ticker, start=start_date, end=end_date)
    return stock_data

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
    
def generate_pdf_report(stock_data,stock_ticker):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(200, 10, txt=f"Stock Report for {stock_ticker}", ln=True, align="C")
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"Stock Price over Time", ln=True, align="C")
    pdf.image(f"{stock_ticker}_close_price.png", x=10, y=50, w=180)
    
    pdf.cell(200, 10, txt=f"Stock Volume over Time", ln=True, align="C")
    pdf.image(f"{stock_ticker}_volume.png", x=10, y=150, w=180)
    
    pdf.cell(200, 10, txt=f"Stock High and Low Price over Time", ln=True, align="C")
    pdf.image(f"{stock_ticker}_high_low.png", x=10, y=250, w=180)
    
    pdf.output(f"{stock_ticker}_report.pdf")


def main():
    #Know The Stock
    stock_ticker = input("Enter the stock ticker: ")
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
    generate_pdf_report(stock_data,stock_ticker)


if __name__ == "__main__":
    main()