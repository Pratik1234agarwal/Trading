import pickle
from datetime import datetime

FILE_NAME = 'transactions'


class Transaction:
    def __init__(self, cash=20000):
        self.holdings = []
        try:
            file = open(FILE_NAME, 'rb')
            self = pickle.load(file)
        except:
            self.transactions = []
            self.cash = cash

    def save(self):
        file = open(FILE_NAME, 'wb')
        pickle.dump(self, file)
        file.close()

    def buy(self, ticker, price, quantity):
        tickers = [i['Ticker'] for i in self.transactions]
        if ticker in tickers:
            return [transaction for transaction in self.transactions if transaction['Ticker'] == ticker][0]
        transaction = {
            'Ticker': ticker,
            'Id': len(self.transactions) + 1,
            'BoughtAt': price,
            "BoughtAtTime": datetime.now(),
            'Holding': True,
            'Quantity': quantity,
            'TransactionValue': quantity * price,
            'SoldAt': 0.00
        }
        if(self.cash < transaction['TransactionValue']):
            return {}
        self.transactions.append(transaction)
        self.cash = self.cash - transaction['TransactionValue']
        self.save()
        return transaction

    def sell(self, ticker, price):
        flag = -1
        temp = {}
        for index, transaction in enumerate(self.transactions):
            if transaction['Ticker'] == ticker:
                flag = index
                temp = transaction
                break

        if not temp['Holding']:
            return temp
        temp['Holding'] = False
        temp['SoldAt'] = price
        temp['pl'] = price - temp['BoughtAt']
        temp['SoldAtTime'] = datetime.now()
        temp['pl_total'] = temp['pl'] * temp['Quantity']
        self.cash = self.cash + temp['TransactionValue']
        self.save()
        return temp

    def get_holdings(self):
        return self.transactions

    def get_unsold_holdings(self):
        trades = []
        for trasaction in self.transactions:
            if trasaction['Holding']:
                trades.append(trasaction)
        return trades

    def get_cash(self):
        return self.cash
