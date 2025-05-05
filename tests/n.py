import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import yfinance as yf
from datetime import date, timedelta

stock1 = input("Enter the first ticker: ").upper()
stock2 = input("Enter the second ticker: ").upper()
ndays = int(input("Enter number of days: "))

start = (date.today() - timedelta(days=ndays+4)).strftime("%Y-%m-%d")
end = (date.today() - timedelta(days=3)).strftime("%Y-%m-%d")

data1 = yf.download(stock1, start=start, end=end)
data2 = yf.download(stock2, start=start, end=end)

data1.reset_index(inplace=True)
data2.reset_index(inplace=True)

pdf_filename = f"{stock1}_{stock2}_comparison.pdf"

with PdfPages(pdf_filename) as pdf:
    plt.figure(figsize=(10, 6))
    plt.plot(data1['Date'], data1['Close'], marker='o', linestyle='-', color='blue', label=f'{stock1} Close')
    plt.plot(data2['Date'], data2['Close'], marker='o', linestyle='--', color='orange', label=f'{stock2} Close')
    plt.title(f'Closing Price Comparison: {stock1} vs {stock2}')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (INR)')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(data1['Date'], data1['High'], marker='o', linestyle='-', color='blue', label=f'{stock1} High')
    plt.plot(data2['Date'], data2['High'], marker='o', linestyle='--', color='orange', label=f'{stock2} High')
    plt.title(f'Daily High Price Comparison: {stock1} vs {stock2}')
    plt.xlabel('Date')
    plt.ylabel('Daily High (INR)')
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    summary1 = data1[['Close', 'High']].describe().round(2)
    summary2 = data2[['Close', 'High']].describe().round(2)

    fig, ax = plt.subplots(figsize=(12, 6))
    plt.axis('off')
    table_data = pd.concat([summary1, summary2], axis=1, keys=[stock1, stock2])
    table = plt.table(cellText=table_data.values,
                      colLabels=table_data.columns,
                      rowLabels=table_data.index,
                      loc='center',
                      cellLoc='center')
    table.scale(1, 2)
    plt.title("Statistical Summary")
    pdf.savefig()
    plt.close()

print(f"Comparison graph and analysis saved as {pdf_filename}")