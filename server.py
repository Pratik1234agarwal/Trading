from flask import Flask, render_template
from app import get_account
from transaction import Transaction
import yfinance as yf

app = Flask(__name__)


def getLatestPrice(acc):
    tickers = [i['Ticker'] for i in acc.transactions]
    data = yf.download(tickers=tickers, progress=False,
                       period="1d", interval='1d')
    return data.Close


@app.route('/')
def index():
    acc = get_account()
    current_price = getLatestPrice(acc)
    print(current_price)
    return render_template('index.html', transactions=acc.transactions, acc=acc, current_price=current_price)


if __name__ == "__main__":
    app.run(debug=False, port=80)
