# -*- coding: utf-8 -*-

class Total(object):
    """docstring for Total"""
    def __init__(self):
        self.p_buy = 0.0  # 買った額(jpy)
        self.n_buy = 0.0  # 買った数(currency)
        self.p_sell = 0.0 # 売った額(jpy)
        self.n_sell = 0.0 # 売った数(currency)

    def getDiffPrice(self):
        return self.p_sell - self.p_buy

    def getSellTotalAverage(self):
        return self.divide(self.p_sell, self.n_sell)

    def getBuyTotalAverage(self):
        return self.divide(self.p_buy, self.n_buy)

    def getSummary(self):
        # 売却額 - 購入額, 売却数, 購入数, 売却額総平均, 購入額総平均
        return self.p_sell - self.p_buy, self.n_sell, self.n_buy, self.divide(self.p_sell, self.n_sell), self.divide(self.p_buy, self.n_buy)

    def buy(self, price, amount):
        self.p_buy += price
        self.n_buy += amount

    def sell(self, price, amount):
        self.p_sell += price
        self.n_sell += amount

    def divide(self, x, y):
        if y == 0:
            return 0
        else:
            return x / y

    def addTotal(self, total):
        self.p_buy += total.p_buy
        self.n_buy += total.n_buy
        self.p_sell += total.p_sell
        self.n_sell += total.n_sell
