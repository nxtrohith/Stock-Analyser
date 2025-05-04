import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import yfinance as yf
from datetime import date, timedelta

# Your existing code
stock = input("Enter the Ticker: ")
ndays = int(input("Days:"))
start = (date.today() - timedelta(days=ndays+4)).strftime("%Y-%m-%d")
end = (date.today() - timedelta(days=3)).strftime("%Y-%m-%d")

data = yf.download(stock, start, end)
data.reset_index(inplace=True)
print(data)

pdf_filename = f"{stock}_graph.pdf"

def close_price():
    with PdfPages(pdf_filename) as pdf:
        plt.figure(figsize=(10, 6))
        plt.plot(data['Date'], data['Close'], marker='o', linestyle='-', color='g', label='Close Price')
        plt.title(f'{stock} Stock Price (Closing) from {start} to {end}')
        plt.xlabel('Date')
        plt.ylabel('Closing Price (INR)')
        plt.grid(True)
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        pdf.savefig()  # Save the current figure into the PDF
        plt.close()
    print(f"Graph saved as {pdf_filename}")

def price_increment():
    with PdfPages(pdf_filename) as pdf:
        plt.figure(figsize=(10, 6))
        plt.plot(data['Date'], data['High'], marker='o', linestyle='-', color='g', label='Daily HIGH (INR)')
        plt.title(f'{stock} Daily Stock day high from {start} to {end}')
        plt.xlabel('Date')
        plt.ylabel('Price Increment (INR)')
        plt.grid(True)
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        pdf.savefig()
        plt.close()
    print(f"Graph saved as {pdf_filename}")

print("1.Closing price graph")
print("2.Price High graph")
typegraph = int(input("Code: "))

if typegraph == 1:
    close_price()
elif typegraph == 2:
    price_increment()
else:
    print("Invalid option selected.")
