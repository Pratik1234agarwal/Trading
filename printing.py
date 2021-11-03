from app import get_account

acc = get_account()


def print_status():
    for a in acc.transactions:
        print("============================================================")
        print(
            f"Ticker: {a['Ticker']} \n Bought At : {a['BoughtAt']} Quantity : {a['Quantity']}")
        print(
            f"Total Value  : {a['TransactionValue']}    InTrade: {a['Holding']} ")
        if a['Holding']:
            print(f"Sold at: {a['SoldAt']}")


print_status()
