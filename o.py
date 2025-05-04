import pandas_datareader as pdr
import datetime
from tiingo import TiingoClient

# Set the API key in your session
import os
config = {}

# To reuse the same HTTP Session across API calls (and have better performance), include a session key.
config['session'] = True
config['api_key'] = "6edd324e5345b0d71cdf56a3163d0a5f05c00c65"
client = TiingoClient(config)
# Set dates
start = datetime.datetime(2024, 4, 23)
end = datetime.datetime(2024, 4, 28)

# Fetch stock data
df = pdr.DataReader('ZOMATO.BO', 'tiingo', start, end)

print(df.head())

articles = client.get_news(tickers=['GOOGL', 'AAPL'],
                            tags=['Laptops'],
                            sources=['washingtonpost.com'],
                            startDate='2017-01-01',
                            endDate='2017-08-31')