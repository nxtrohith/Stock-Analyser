import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import date,timedelta

# Your existing code
stock = input("Enter the Ticker: ")
ndays = int(input("Days:"))
start = (date.today() - timedelta(days=ndays+4)).strftime("%Y-%m-%d")
end = (date.today() - timedelta(days=3)).strftime("%Y-%m-%d")

data = yf.download(stock, start, end)
data.reset_index(inplace=True)
print(data)

def close_price():
    # Plotting the Adjusted Close price against the Date
    plt.figure(figsize=(10, 6))  # Set the figure size
    plt.plot(data['Date'], data['Close'], marker='o', linestyle='-', color='g', label='Close Price')
    plt.title(f'{stock} Stock Price (Closing) from {start} to {end}')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (INR)')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.show()

def price_increment():
    # Plotting the price increment graph
    plt.figure(figsize=(10, 6))
    plt.plot(data.Date,data.High, marker='o', linestyle='-', color='g', label='Daily HIGH (INR)')
    plt.title(f'{stock} Daily Stock day high from {start} to {end}')
    plt.xlabel('Date')
    plt.ylabel('Price Increment (INR)')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
print("1.Closing price graph")
print("2.Price High graph")
typegraph = int(input("Code: "))

if typegraph == 1:
    close_price()
if typegraph == 2:
    price_increment()