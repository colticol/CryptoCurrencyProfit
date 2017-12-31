# -*- coding: utf-8 -*-
import pandas as pd

class JPY(object):
    """docstring for JPY"""
    def __init__(self, usd_filename, btc_filename, bch_filename):
        usd = pd.read_csv(usd_filename, parse_dates=['snapped_at'])
        btc = pd.read_csv(btc_filename, parse_dates=['snapped_at'])
        bch = pd.read_csv(bch_filename, parse_dates=['snapped_at'])
        self.jpy = pd.merge(pd.merge(btc, bch, how='left'), usd, how='left')

    def getJPY(self):
        return self.jpy
