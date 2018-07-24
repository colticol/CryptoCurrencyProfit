# -*- coding: utf-8 -*-
import pandas as pd
from exchange import Exchange


class BitFlyer(Exchange):
    """docstring for BitFlyer"""
    def __init__(self, f_trades, jpy):
        self.trades = pd.read_csv(f_trades, parse_dates=['取引日時'])

    def calcTotal(self, controller):
        # for trades
        for _, row in self.getTrades().iterrows():
            price = row['価格']
            # Set Dictionary
            currency, unit = row['通貨'].split('/')
            # Buy or Sell
            if row[currency] > 0:  # buy
                controller.buy(currency, price * abs(row[currency]), abs(row[currency]))
                controller.sell(unit, price * abs(row[currency]), abs(row['JPY']))
            elif row[currency] < 0:  # sell
                controller.sell(currency, price * abs(row[currency]), abs(row[currency]))
                controller.buy(unit, price * abs(row[currency]), abs(row['JPY']))
        return controller
