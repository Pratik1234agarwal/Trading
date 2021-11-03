
import time
import yfinance as yf
import pandas as pd
from tickers import TICKERS
from indicators import ema
from transaction import Transaction
import math
import asyncio
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager
import pickle
from datetime import datetime

# Variables and Constant
CASH = 10000  # Account Size
CASH_PER_TRADE = 5000  # Cash Usage Per Trade
# If the trade amount is less than this don't take trade, charges would exceed.
CASH_MIN_TRADE = 2000


# TODO Ahead
# 1. Choose between trades, if multiple exists
# 2. Update the stocks trade win percentage real time for better stock selection
# 3. Do not pick a stock with win pt < 5%
# 4. Add a database system for better performance.


def signal(history):
    if(len(history) < 52):
        return False
    ema13 = ema(history, 13)
    ema50 = ema(history, 50)
    ema13 = ema13[50-11:]
    ema50 = ema50[2:]
    if(ema13[-1] < ema50[-1] and history[-1] > ema50[-1] and history[-2] < ema50[-2]):
        return True
    else:
        return False


FILE_NAME = 'transactions'


def get_account():
    try:
        file = open(FILE_NAME, 'rb')
        account = pickle.load(file)
        return account
    except:
        account = Transaction()
        account.save()
        return account


def date_manipulation():
    date = datetime.now()
    print(date)
    time = date.now().time()
    minute = time.minute
    remaining = 0
    if minute < 15:
        remaining = 15 - minute
    elif minute >= 15 and minute < 30:
        remaining = 30 - minute
    elif minute >= 30 and minute < 45:
        remaining = 45 - minute
    else:
        remaining = 60 - minute
    remaining = (remaining - 1) * 60
    seconds = time.second
    remaining = remaining + (40 - seconds)
    return remaining


def main():
    c = 0
    while True:
        if c != 0:
            print("====================================================")
            print("Running at : ", datetime.now())
            account = get_account()
            start = time.time()
            data = yf.download(tickers=TICKERS, period="3d",
                               interval="15m", progress=False)
            data = data.dropna()
            print(f"Data Downloaded in time {time.time() - start}s")
            for ticker in TICKERS:
                if account.get_cash() > CASH_MIN_TRADE and signal(data.Close[ticker].values):
                    CASH_TO_BE_BURNT = 0
                    price = data.Close[ticker].values[-1]
                    if account.get_cash() < CASH_PER_TRADE:
                        CASH_TO_BE_BURNT = account.get_cash()
                    else:
                        CASH_TO_BE_BURNT = CASH_PER_TRADE
                    account.buy(ticker, price, math.floor(
                        CASH_TO_BE_BURNT / price))
                    print("===============================")
                    print(f"Stock Bought {ticker} at price: {price}")
                    print(f"Cash Left = {account.get_cash()}")
            time.sleep(60)
        remaining = date_manipulation()
        c += 1
        print(f"Sleeping for {remaining} seconds")
        time.sleep(remaining)


def sell():
    while True:
        account = get_account()
        # Monitor if a trade is made
        trades = account.get_unsold_holdings()
        if len(trades) > 0:

            data = yf.download(tickers=[a['Ticker']
                               for a in trades], period="1d", interval="1d", progress=False)
            data = data.dropna()
            for trade in trades:
                price_buy = trade['BoughtAt']
                current = 0
                if len(trades) == 1:
                    current = data.Close.values[-1]
                else:
                    current = data.Close[trade['Ticker']].values[-1]
                pt = (current - price_buy) / price_buy
                if pt >= 0.05 or pt <= -0.03:
                    account.sell(trade['Ticker'], current)
                    print(f"Stock {trade['Ticker']} Sold at: {current}")
        time.sleep(2)


if __name__ == "__main__":
    p1 = Process(target=main)
    p2 = Process(target=sell)

    p1.start()
    p2.start()
