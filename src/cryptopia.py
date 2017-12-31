# -*- coding: utf-8 -*-
import pandas as pd
from exchange import Exchange
from total import Total


class Cryptopia(Exchange):
    """docstring for Cryptopia"""
    def __init__(self, name, f_trades, jpy):
        super().__init__(name)
        self.setTrades(f_trades, jpy)

    def __init__(self, name, f_trades, f_withdraws, jpy):
        super().__init__(name)
        self.setTrades(f_trades, jpy)
        self.setWithdraws(f_withdraws, jpy)

    def setTrades(self, f_trades, jpy):
        self.trades = pd.read_csv(f_trades, parse_dates=['Timestamp'], dayfirst=True)
        self.trades['Timestamp'] += pd.offsets.BDay(normalize=True)
        self.trades = pd.merge(pd.merge(self.trades, jpy.getBTC(), left_on='Timestamp', right_on='snapped_at'), jpy.getBCH(), left_on='Timestamp', right_on='snapped_at')

    def setWithdraws(self, f_withdraws, jpy):
        self.withdraws = pd.read_csv(f_withdraws, parse_dates=['Timestamp'], dayfirst=True)
        self.withdraws['Timestamp'] += pd.offsets.BDay(normalize=True)
        self.withdraws = pd.merge(pd.merge(self.withdraws, jpy.getBTC(), left_on='Timestamp', right_on='snapped_at'), jpy.getBCH(), left_on='Timestamp', right_on='snapped_at')

    def calcResult(self):
        result = {'Fee':0.0}
        # for trades
        for _, row in self.getTrades().iterrows():
            # Set Dictionary
            currency, unit = row['Market'].split('/')
            if currency not in result:
                result[currency] = Total()
            if unit not in result:
                result[unit] = Total()
            # Set Currency
            try:
                unit_price = row['p' + unit]
            except Exception as e:
                print('[Cryptopia]: Unknown Unit ' + unit)
                continue
            # Calculate Fee
            result['Fee'] += unit_price * abs(row['Fee'])
            # Buy or Sell
            if row['Type'] == 'Buy':
                result[currency].buy(unit_price * row['Total'], row['Amount'])
                result[unit].sell(unit_price * row['Total'], row['Total'])
            elif row['Type'] == 'Sell':
                result[currency].sell(unit_price * row['Total'], row['Amount'])
                result[unit].buy(unit_price * row['Total'], row['Total'])
            else:
                print('[Cryptopia]: Unknown Type ' + row['Type'])
        # for withdraws
        if self.getWithdraws() is not False:
            for _, row in self.getWithdraws().iterrows():
                try:
                    result['Fee'] += row['p' + row['Currency']] * abs(row['Fee'])
                except Exception as e:
                    print('[Cryptopia]: Unknown FeeCurrency ' + currency)
        self.result = result
        return result
