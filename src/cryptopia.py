# -*- coding: utf-8 -*-
import pandas as pd
from exchange import Exchange


class Cryptopia(Exchange):
    """docstring for Cryptopia"""
    def __init__(self, f_trades, jpy):
        self.trades = pd.read_csv(f_trades, parse_dates=['Timestamp'], dayfirst=True)
        self.trades['Timestamp'] = self.trades['Timestamp'].dt.normalize()
        self.trades = pd.merge(self.trades, jpy.getJPY(), left_on='Timestamp', right_on='snapped_at', how='left')

    def calcTotal(self, controller):
        # for trades
        for _, row in self.getTrades().iterrows():
            # Set Dictionary
            currency, unit = row['Market'].split('/')
            # Set Currency
            try:
                unit_price = row['p' + unit]
            except Exception as e:
                print('[Cryptopia]: Unknown Unit ' + unit)
                continue
            # Buy or Sell
            if row['Type'] == 'Buy':
                controller.buy(currency, unit_price * row['Total'], row['Amount'])
                controller.sell(unit, unit_price * row['Total'], row['Total'])
            elif row['Type'] == 'Sell':
                controller.sell(currency, unit_price * row['Total'], row['Amount'])
                controller.buy(unit, unit_price * row['Total'], row['Total'])
            else:
                print('[Cryptopia]: Unknown Type ' + row['Type'])
        return controller
