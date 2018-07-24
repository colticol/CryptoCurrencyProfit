# -*- coding: utf-8 -*-
from total import Total


class Controller(object):
    """docstring for Controller"""
    def __init__(self, exchanges):
        self.exchanges = exchanges
        self.currencies = False

    def calcExchangeResult(self):
        for exchange in self.exchanges:
            exchange.calcResult()

    def printExchangeSummary(self):
        print('Exchange Summary')
        for exchange in self.exchanges:
            print(exchange.getName())
            for currency, total in exchange.getResult().items():
                if currency == 'Fee':
                    print(currency, total)
                else:
                    print(currency, total.getSummary())

    def calcTotalExchangeResult(self):
        trades = {'Fee':0.0}
        for exchange in self.exchanges:
            for currency, total in exchange.getResult().items():
                if currency == 'Fee':
                    trades['Fee'] += total
                else:
                    if currency not in trades:
                        trades[currency] = Total()
                    trades[currency].addTotal(total)
        self.currencies = trades

    def printTotalExchangeSummary(self):
        print('Total Exchange Summary')
        for currency, total in self.currencies.items():
            if currency == 'Fee':
                print(currency, total)
            else:
                print(currency, total.getSummary())

    def calcProfit(self, jpy_deposit, jpy_withdrow, hold):
        profit = 0.0
        for currency, amount in hold.items():
            currency = self.currencies[currency]
            if amount > 0:
                profit += currency.getBuyTotalAverage() * amount
            else:
                profit += currency.getSellTotalAverage() * amount
        return profit + jpy_withdrow - jpy_deposit
