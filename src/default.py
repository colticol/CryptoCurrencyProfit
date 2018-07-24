# -*- coding: utf-8 -*-
import pandas as pd
import re
from exchange import Exchange
from total import Total


class Default(Exchange):
    """docstring for Zaif"""
    def __init__(self, holds, price):
        super().__init__('defalut')
        result = {}
        for currency, amount in holds.items():
            price = price[currency]
            if currency not in result:
                result[currency] = Total()
            result[currency].buy(price * amount, amount)
        self.result = result

    def calcResult(self):
        return self.result
