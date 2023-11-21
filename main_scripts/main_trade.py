from database.adatabase import ADatabase
from processor.processor import Processor as p
from extractor.alp_extractor import ALPExtractor as alp
from datetime import datetime, timedelta
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
from random import shuffle
from time import sleep

live = False

trades = pd.read_csv("trades.csv")
seats = trades.tail(1)
account = alp.account()
cash = float(account["cash"])

for row in seats.iterrows():
    direction = row[1]["direction"]
    ticker = row[1]["ticker"]
    adjclose = row[1]["adjclose"]
    date = row[1]["date"]
    qty = int(cash/adjclose)
    amount = qty * adjclose
    if direction == 1:
        print(date,ticker,adjclose,qty,amount,"buy")
        # alp.buy(ticker,qty)
    else:
        print(date,ticker,adjclose,qty,amount,"sell")
        # alp.sell(ticker,qty)

if live:
    alp.close()
    sleep(300)
    for row in seats.iterrows():
        direction = row[1]["direction"]
        ticker = row[1]["ticker"]
        adjclose = row[1]["adjclose"]
        date = row[1]["date"]
        qty = int(cash/adjclose)
        amount = qty * adjclose
        if direction == 1:
            print(date,ticker,adjclose,qty,amount,"buy")
            alp.buy(ticker,qty)
        else:
            print(date,ticker,adjclose,qty,amount,"sell")
            alp.sell(ticker,qty)    