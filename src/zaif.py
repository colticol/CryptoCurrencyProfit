# -*- coding: utf-8 -*-
import pandas as pd
import re
from exchange import Exchange


class Zaif(Exchange):
    """docstring for Zaif"""
    def __init__(self, f_trades, jpy):
        self.trades = pd.read_csv(f_trades, parse_dates=['日時'])
        self.trades['日時'] = self.trades['日時'].dt.normalize()
        self.trades = pd.merge(self.trades, jpy.getJPY(), left_on='日時', right_on='snapped_at', how='left')

    def calcTotal(self, controller):
        # for trades
        for _, row in self.getTrades().iterrows():
            # Set Currency Unit
            unit_amount, unit = self.splitUnitCurrency(row['価格'])
            if unit == 'BTC' or unit == 'BCH':
                price = unit_amount * row['p' + unit]
            elif unit == 'JPY':
                price = unit_amount * 1.0
            else:
                print('[Zaif]: Unknown 価格 ' + row['価格'])
            # Set Dictionary
            amount, currency = self.splitUnitCurrency(row['数量'])
            # Buy or Sell
            if row['注文'] ==  '買い':  # buy
                controller.buy(currency, price * amount, amount)
                controller.sell(unit, price * amount, price * amount)
            elif row['注文'] == '売り':  # sell
                controller.sell(currency, price * amount, amount)
                controller.buy(unit, price * amount, price * amount)
        return controller

    def splitUnitCurrency(self, s):
        index = re.search('[A-Z]', s).start()
        return float(s[:index]), s[index:]
