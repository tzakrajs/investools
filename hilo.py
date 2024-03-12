#!/usr/bin/env python3
"""
This script uses the Alpha Vantage API to get the last 
100 days of daily data for a given stock symbol, and 
calculates the average curve (close/open) for the period.
"""

import requests
import pandas as pd

# Get API_KEY from environment variable
import os
API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')

# Get SYMBOL from argument
import sys
try:
    SYMBOL = sys.argv[1]
except IndexError:
    print('Please provide a stock symbol as an argument')
    sys.exit(1)

# Setup the API call for daily data
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}'

# Make the request
response = requests.get(url)
data = response.json()

# Assuming the response structure, extract the last 100 days of daily data
time_series = data['Time Series (Daily)']
dates = list(time_series.keys())

# Prepare lists to store the extracted data
opens, highs, closes, curves = [], [], [], []

for date in dates:
    day_data = time_series[date]
    open = float(day_data['1. open'])
    close = float(day_data['4. close'])
    opens.append(open)
    highs.append(float(day_data['2. high']))
    closes.append(close)
    curves.append(close/open)

# Optionally, create a DataFrame for easy visualization
df = pd.DataFrame({
    'Date': dates,
    'Open': opens,
    'High': highs,
    'Close': closes,
    'Curve': curves
})

# Show the DataFrame
print(df)

# Get average curve
average_curve = sum(curves) / len(curves)
print(f'Average curve: {average_curve}')
if average_curve > 1:
    print('The stock is closing higher than it opens on average')
else:
    print('The stock is closing lower than it opens on average')