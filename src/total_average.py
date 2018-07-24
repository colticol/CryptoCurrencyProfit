# -*- coding: utf-8 -*-
from jpy import JPY
from bitfinex import BitFinex
from cryptopia import Cryptopia
from bitflyer import BitFlyer
from zaif import Zaif
from total import Total
from total_controller import TotalController


def getDefaultDict(holds, prices):
    default = {}
    for currency, amount in holds.items():
        price = prices[currency]
        default[currency] = Total()
        default[currency].buy(price * amount, amount)
    return default


def main():
    # Set Last Year Holds and Total Average
    last_holds = {}
    last_price = {}
    # Set JPY Withdraw and Deposit
    jpy_deposit  = 3000000
    jpy_withdraw = 0
    # Set Holds
    holds = {'BTC':0.0001, 'BCH':45.37983532, 'ZAIF':2154694.4}

     # Initialize Controller
    default = getDefaultDict(last_holds, last_price)
    controller = TotalController(default)

    # Read JPY/USD, BTC/JPY, BCH/JPY
    jpy = JPY('../data/2017/jpy/USDJPY.csv', '../data/2017/jpy/btc-jpy-max.csv', '../data/2017/jpy/bch-jpy-max.csv')
    # Join JPY Data When Read History of Each Exchange
    # Read Trade (and Withdraw) History of Bitfinex
    bitfinex = BitFinex('../data/2017/bitfinex/2017-12-28-trades.csv', jpy)
    # Read Trade (and Withdraw) History of Cryptopia
    cryptopia = Cryptopia('../data/2017/cryptopia/Trade_History.csv', jpy)
    # Read Trade (and Withdraw) History of Bitflyer
    bitflyer = BitFlyer('../data/2017/bitflyer/TradeHistory_20171228.csv', jpy)
    # Read Trade (and Withdraw) History of Zaif
    zaif = Zaif('../data/2017/zaif/trade.csv', jpy)

    # Calculate All Total
    exchanges = [bitfinex, cryptopia, bitflyer, zaif]
    for exchange in exchanges:
        controller = exchange.calcTotal(controller)
    # Print Summary
    controller.printSummary()
    # Calculate Profit
    print('Profit :', controller.calcProfit(jpy_deposit, jpy_withdraw, holds))


if __name__ == '__main__':
    main()
