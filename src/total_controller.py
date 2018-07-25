# -*- coding: utf-8 -*-
from total import Total

class TotalController(object):
    """
        docstring for TotalController
        control Total of all currencies (includes JPY)
        calcurate total average
    """
    def __init__(self, default):
        self.total_dict = default

    def buy(self, currency, price, amount):
        if currency not in self.total_dict:
            self.total_dict[currency] = Total()
        self.total_dict[currency].buy(price, amount)

    def sell(self, currency, price, amount):
        if currency not in self.total_dict:
            self.total_dict[currency] = Total()
        self.total_dict[currency].sell(price, amount)

    def getBuyTotalAverage(self, currency):
        return self.total_dict[currency].getBuyTotalAverage()

    def getSellTotalAverage(self, currency):
        return self.total_dict[currency].getSellTotalAverage()

    def printSummary(self):
        print('通貨 : 売却数\t購入数\t売却額総平均\t購入額総平均')
        for currency, total in self.total_dict.items():
            print ('{0} : {1}\t{2}\t{3}\t{4}'.format(currency, total.getSellAmount(), total.getBuyAmount(), total.getSellTotalAverage(), total.getBuyTotalAverage()))

    def calcProfit(self, funds, assets):
        profit = 0.0
        for currency, amount in assets.items():
            if amount < 0:
                print('calcProfit : invalid amount [{0}]'.format(amount))
            elif currency == 'JPY':
                profit += 1.0 * amount
            else:
                total = self.total_dict[currency]
                profit += total.getBuyTotalAverage() * amount
        return profit - funds
