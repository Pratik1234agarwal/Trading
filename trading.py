# Importing important Packages
import yfinance as yf
import pandas as pd
import time
from tickers import TICKERS


# Variables and Constant
CASH = 10000  # Account Size
CASH_PER_TRADE = 5000  # Cash Usage Per Trade
# If the trade amount is less than this don't take trade, charges would exceed.
CASH_MIN_TRADE = 2000
Transactions = {}
# Trasaction = Object
# {
#  Date:Date,ticker:ticker,boughtAt:float
# ,holding:boolean,soldAt:float,pl:float,trasaction_value:flaot
# }
#
