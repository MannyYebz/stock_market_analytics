# Stock Market Analysis — AAPL Deep Dive
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import time

os.makedirs('charts', exist_ok=True)


def timer(func):
    def wrapper(*args,**kwargs):
        start = time.time()
        result = func(*args,**kwargs)
        end = time.time()
        print(f'{func.__name__} took {end - start:.2f} seconds')
        return result
    return wrapper

#df = pd.read_csv('wspd.csv')
'''This is the professional workflow 
   to get a general overview
   of the data you are working on
   .Do this with any dataset you are given'''

# print(df.shape)          # how many rows and columns
# print(df.columns.tolist()) # all column names
# print(df.head())         # first 5 rows
# print(df.info())         # data types
# print(df.describe())     # statistical summary


@timer
def load_data():
    # load csv, filter for AAPL, drop Capital Gains
    # convert date, sort, set index
    # return aapl
    df = pd.read_csv('wspd.csv')
    df['Date'] = pd.to_datetime(df['Date'], utc=True)
    aapl = df[df["Ticker"] == "AAPL"]
    aapl = aapl.drop('Capital Gains', axis=1)
    aapl = aapl.sort_values('Date')
    aapl = aapl.set_index('Date')
    aapl = aapl[~aapl.index.duplicated(keep='first')]
    return aapl


def calculate_metrics(df, start_date='2020-01-01'):
    # we'll fill this in next
    # Finding the moving averages to see trends
    
    df['MA90'] = df['Close'].rolling(window=90).mean()
    df['MA180'] = df['Close'].rolling(window=180).mean()
    df['MA270'] = df['Close'].rolling(window=270).mean()
    df['MA360'] = df['Close'].rolling(window=360).mean()
    
    # Daily return - how much percentage did the stock move each day?
    df['Daily_Return'] = df['Close'].pct_change() * 100

    # Volatility - rolling 30-day standard deviation of daily returns
    df['Volatility'] = df['Daily_Return'].rolling(window=30).std()

    # choose beginning date as a reference frame
    df = df[df.index >= start_date]

    return df

def get_insights(df):
    # we'll fill this in next
    pass

def plot_charts(df):
    # we'll fill this in next
    pass

if __name__ == '__main__':
    df = load_data()
    df = calculate_metrics(df,start_date='2020-01-01')
    print(df[['Close','MA90','MA180','MA270','MA360','Daily_Return','Volatility']].tail(10))