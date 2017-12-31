# -*- coding: utf-8 -*-
import pandas as pd

class JPY(object):
    """docstring for JPY"""
    def __init__(self, usd_filename, btc_filename, bch_filename):
        self.usd = pd.read_csv(usd_filename, parse_dates=['snapped_at'])
        self.btc = pd.read_csv(btc_filename, parse_dates=['snapped_at'])
        self.bch = pd.read_csv(bch_filename, parse_dates=['snapped_at'])

    def getUSD(self):
        return self.usd

    def getBTC(self):
        return self.btc

    def getBCH(self):
        return self.bch
