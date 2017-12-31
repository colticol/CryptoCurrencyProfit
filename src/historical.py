# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

class Historical(object):
    """docstring for CoinGekko"""
    def __init__(self, filename):
        self.usdjpy = pd.read_csv(filename, parse_dates=['Date'])

    def getUSDJPY(self):
        return self.usdjpy
