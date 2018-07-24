# -*- coding: utf-8 -*-
import pandas as pd
from exchange import Exchange


class BitFinex(Exchange):
    """docstring for BitFinex"""
    def __init__(self, f_trades, jpy):
        self.trades = pd.read_csv(f_trades, parse_dates=['Date'])
        self.trades['Date'] = self.trades['Date'].dt.normalize()
        self.trades = pd.merge(self.getTrades(), jpy.getJPY(), left_on='Date', right_on='snapped_at', how='left')

    def calcTotal(self, controller):
        for _, row in self.getTrades().iterrows():
            # Set Dictionary
            pair = row['Pair']
            currency, unit = row['Pair'].split('/')
            # Set Unit Price
            try:
                unit_price = row['p' + unit]
            except Exception as e:
                print('[BitFinex]: Unknown Unit ' + unit)
                continue
            # Buy or Sell
            if row['Amount'] > 0:  # buy
                controller.buy(currency, abs(unit_price * row['Price'] * row['Amount']), abs(row['Amount']))
                controller.sell(unit, abs(unit_price * row['Price'] * row['Amount']), abs(row['Price'] * row['Amount']))
            elif row['Amount'] < 0:  # sell
                controller.sell(currency, abs(unit_price * row['Price'] * row['Amount']), abs(row['Amount']))
                controller.buy(unit, abs(unit_price * row['Price'] * row['Amount']), abs(row['Price'] * row['Amount']))
        return controller
