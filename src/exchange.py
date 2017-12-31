# -*- coding: utf-8 -*-


class Exchange(object):
    """docstring for Exchange"""
    def __init__(self, name):
        self.name = name
        self.trades = False
        self.deposits = False
        self.withdraws = False
        self.merged = False
        self.result = False

    def getName(self):
        return self.name

    def getTrades(self):
        return self.trades

    def getDeposits(self):
        return self.deposits

    def getWithdraws(self):
        return self.withdraws

    def getMerged(self):
        return self.merged

    def getResult(self):
        return self.result

    # @abstractmethod
    def calcResult(self):
        pass
