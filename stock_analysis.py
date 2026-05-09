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

@timer
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

@timer
def get_insights(df):
    latest = df.iloc[-1]  # grabs the most recent row

    close    = latest['Close']
    ma90     = latest['MA90']
    ma180    = latest['MA180']
    ma270    = latest['MA270']
    ma360    = latest['MA360']
    vol      = latest['Volatility']
    ret      = latest['Daily_Return']

    print('===== AAPL INSIGHTS =====')
    print(f"Latest Close:  ${close:.2f}")
    print(f"MA90:          ${ma90:.2f}")
    print(f"MA180:         ${ma180:.2f}")
    print(f"MA270:         ${ma270:.2f}")
    print(f"MA360:         ${ma360:.2f}")

    # Trend signal
    if close > ma90 > ma180 > ma270 > ma360:
        print("Trend:         BULLISH — price is above all moving averages")
    elif close < ma90 < ma180 < ma270 < ma360:
        print("Trend:         BEARISH — price is below all moving averages")
    else:
        print("Trend:         MIXED — price is between moving averages")

    # Volatility signal
    if vol > 3:
        print(f"Volatility:    HIGH ({vol:.2f}) — market is uncertain")
    else:
        print(f"Volatility:    NORMAL ({vol:.2f})")

    # Last day signal
    if ret > 0:
        print(f"Last Return:   +{ret:.2f}% (up day)")
    else:
        print(f"Last Return:   {ret:.2f}% (down day)")

    print('=========================')

@timer
def plot_charts(df):
    # we'll fill this in next
    #create 3 charts stacked vertically, sharing the same x-axis (date)
    fig, (ax1,ax2,ax3) = plt.subplots(3,1,figsize=(14,10),sharex=True)

    #chart 1 - closing price with all moving averages
    ax1.plot(df.index, df['Close'], label='Close', color = 'black', linewidth=1)
    ax1.plot(df.index, df['MA90'], label='MA90', color = 'black', linestyle='--')
    ax1.plot(df.index, df['MA180'], label='MA180', color = 'black', linestyle='--')
    ax1.plot(df.index, df['MA270'], label='MA270', color = 'black', linestyle='--')
    ax1.plot(df.index, df['MA360'], label='MA360', color = 'black', linestyle='--')
    ax1.set_title('AAPL Price & Moving Averages')
    ax1.set_ylabel('Price ($)')
    ax1.legend()

    # Chart 2 — Daily return percentage
    ax2.plot(df.index, df['Daily_Return'], color='blue', linewidth=0.8)
    ax2.axhline(0, color='red', linestyle='--', linewidth=0.8)  # zero line for reference
    ax2.set_title('Daily Return %')
    ax2.set_ylabel('Return (%)')

    # Chart 3 — Rolling volatility
    ax3.plot(df.index, df['Volatility'], color='orange', linewidth=0.8)
    ax3.set_title('30-Day Rolling Volatility')
    ax3.set_ylabel('Volatility (%)')

    plt.tight_layout()  # prevents charts from overlapping
    plt.savefig('charts/aapl_analysis.png')
    plt.show()
    

if __name__ == '__main__':
    df = load_data()
    print('--'*50)
    print('\n')
    df = calculate_metrics(df,start_date='2020-01-01')
    print('--'*50)
    print('\n')
    print(df[['Close','MA90','MA180','MA270','MA360','Daily_Return','Volatility']].tail(10))
    print('--'*50)
    print('\n')
    plot_charts(df)
    print('--'*50)
    print('\n')
    get_insights(df)