# -*- coding: utf-8 -*-


class Exchange(object):
    """docstring for Exchange"""
    def __init__(self):
        self.trades = False

    def getTrades(self):
        return self.trades

    # @abstractmethod
    def calcTotal(self, controller):
        pass
