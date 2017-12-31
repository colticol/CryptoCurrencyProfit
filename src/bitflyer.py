# -*- coding: utf-8 -*-
import pandas as pd
from exchange import Exchange
from total import Total


class BitFlyer(Exchange):
    """docstring for BitFlyer"""
    def __init__(self, name, f_trades):
        super().__init__(name)
        self.setTrades(f_trades)

    def __init__(self, name, f_trades, f_withdraws, jpy):
        super().__init__(name)
        self.setTrades(f_trades)
        self.setWithdraws(f_withdraws, jpy)

    def setTrades(self, f_trades):
        self.trades = pd.read_csv(f_trades, parse_dates=['取引日時'])

    def setWithdraws(self, f_withdraws, jpy):
        self.withdraws = pd.read_csv(f_withdraws, parse_dates=['取引日時'])
        self.withdraws['取引日時'] += pd.offsets.BDay(normalize=True)
        self.withdraws = pd.merge(self.withdraws, jpy.getJPY(), left_on='取引日時', right_on='snapped_at', how='left')

    def calcResult(self):
        result = {'Fee':0.0}
        # for trades
        for _, row in self.getTrades().iterrows():
            price = row['価格']
            # Set Dictionary
            currency, unit = row['通貨'].split('/')
            if currency not in result:
                result[currency] = Total()
            if unit not in result:
                result[unit] = Total()
            # Calculate Fee
            result['Fee'] += price * abs(row['手数料({})'.format(currency)])
            # Buy or Sell
            if row[currency] > 0:  # buy
                result[currency].buy(price * abs(row[currency]), abs(row[currency]))
                result[unit].sell(price * abs(row[currency]), abs(row['JPY']))
            elif row[currency] < 0:  # sell
                result[currency].sell(price * abs(row[currency]), abs(row[currency]))
                result[unit].buy(price * abs(row[currency]), abs(row['JPY']))
        # for withdraws
        if self.getWithdraws() is not False:
            for _, row in self.getWithdraws().iterrows():
                if row['通貨等'] == 'BTC' or row['通貨等'] == 'BCH':
                    result['Fee'] += row['p' + row['通貨等']] * abs(row['手数料合計'])
                elif row['通貨等'] == 'JPY':
                    result['Fee'] += abs(row['手数料合計'])
                else:
                    print('[bitflyer] Invalid 通貨等 ' + row['通貨等'])
        self.result = result
        return result
