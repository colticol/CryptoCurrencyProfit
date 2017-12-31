# -*- coding: utf-8 -*-
import pandas as pd
import re
from exchange import Exchange
from total import Total


class Zaif(Exchange):
    """docstring for Zaif"""
    def __init__(self, name, f_trades, jpy):
        super().__init__(name)
        self.setTrades(f_trades, jpy)

    def __init__(self, name, f_trades, f_withdraws, jpy):
        super().__init__(name)
        self.setTrades(f_trades, jpy)
        self.setWithdraws(f_withdraws, jpy)

    def setTrades(self, f_trades, jpy):
        self.trades = pd.read_csv(f_trades, parse_dates=['日時'])
        self.trades['日時'] += pd.offsets.BDay(normalize=True)
        self.trades = pd.merge(self.trades, jpy.getBTC(), left_on='日時', right_on='snapped_at', how='left')

    def setWithdraws(self, f_withdraws, jpy):
        self.withdraws = pd.read_csv(f_withdraws, parse_dates=['日時'])
        self.withdraws['日時'] += pd.offsets.BDay(normalize=True)
        self.withdraws = pd.merge(self.withdraws, jpy.getBTC(), left_on='日時', right_on='snapped_at', how='left')

    def calcResult(self):
        result = {'Fee':0.0}
        # for trades
        for _, row in self.getTrades().iterrows():
            # Calculate Fee
            if row['手数料'] == row['手数料']:
                amount, currency = self.splitUnitCurrency(row['手数料'])
                if currency == 'BTC' or currency == 'BCH':
                    result['Fee'] += row['p' + currency] * amount
                elif currency == 'JPY':
                    result['Fee'] += 1.0 * amount
                else:
                    print('[Zaif]: Unknown 手数料 ' + row['手数料'])
            # Calculate Bonus
            if row['ボーナス'] == row['ボーナス']:
                bonus = float(row['ボーナス'].replace('円', ''))
                result['Fee'] -= bonus
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
            if currency not in result:
                result[currency] = Total()
            if unit not in result:
                result[unit] = Total()
            # Buy or Sell
            if row['注文'] ==  '買い':  # buy
                result[currency].buy(price * amount, amount)
                result[unit].sell(price * amount, price * amount)
            elif row['注文'] == '売り':  # sell
                result[currency].sell(price * amount, amount)
                result[unit].buy(price * amount, price * amount)
        # for withdraws
        if self.getWithdraws() is not False:
            for _, row in self.getWithdraws().iterrows():
                amount, currency = self.splitUnitCurrency(row['手数料'])
                if currency == 'BTC' or currency == 'BCH':
                    result['Fee'] += row['p' + currency] * amount
                elif currency == 'JPY':
                    result['Fee'] += amount
                else:
                    print('[Zaif] Invalid 手数料 ' + row['手数料'])
        self.result = result
        return result

    def splitUnitCurrency(self, s):
        index = re.search('[A-Z]', s).start()
        return float(s[:index]), s[index:]
