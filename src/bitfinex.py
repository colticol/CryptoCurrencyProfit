# -*- coding: utf-8 -*-
import pandas as pd
from exchange import Exchange
from total import Total


class BitFinex(Exchange):
    """docstring for BitFinex"""
    def __init__(self, name, f_trades, jpy):
        super().__init__(name)
        self.setTrades(f_trades, jpy)

    def setTrades(self, f_trades, jpy):
        self.trades = pd.read_csv(f_trades, parse_dates=['Date'])
        self.trades['Date'] += pd.offsets.Day(0, normalize=True)
        self.trades = pd.merge(self.getTrades(), jpy.getJPY(), left_on='Date', right_on='snapped_at', how='left')

    def calcResult(self):
        result = {'Fee':0.0}
        for _, row in self.getTrades().iterrows():
            # Set Dictionary
            pair = row['Pair']
            currency, unit = row['Pair'].split('/')
            if currency not in result:
                result[currency] = Total()
            if unit not in result:
                result[unit] = Total()
            # Calcurate Fee
            try:
                result['Fee'] += row['p' + row['FeeCurrency']] * abs(row['Fee'])
            except Exception as e:
                print('[BitFinex]: Unknown Fee Currency ' + row['FeeCurrency'])
            # Set Unit Price
            try:
                unit_price = row['p' + unit]
            except Exception as e:
                print('[BitFinex]: Unknown Unit ' + unit)
                continue
            # Buy or Sell
            if row['Amount'] > 0:  # buy
                result[currency].buy(abs(unit_price * row['Price'] * row['Amount']), abs(row['Amount']))
                result[unit].sell(abs(unit_price * row['Price'] * row['Amount']), abs(row['Price'] * row['Amount']))
            elif row['Amount'] < 0:  # sell
                result[currency].sell(abs(unit_price * row['Price'] * row['Amount']), abs(row['Amount']))
                result[unit].buy(abs(unit_price * row['Price'] * row['Amount']), abs(row['Price'] * row['Amount']))
        self.result = result
        return result
