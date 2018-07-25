# -*- coding: utf-8 -*-
from jpy import JPY
from bitfinex import BitFinex
from cryptopia import Cryptopia
from bitflyer import BitFlyer
from zaif import Zaif
from total import Total
from total_controller import TotalController


def setLastYear(holds, prices):
    default = {}
    value = 0
    for currency, amount in holds.items():
        price = prices[currency]
        default[currency] = Total()
        default[currency].buy(price * amount, amount)
        value += price * amount
    return default, value


def main():
    # Set Last Year Holds and Total Average
    last_holds = {'JPY':10000, 'BTC':1.0}
    last_price = {'JPY':1.0, 'BTC':1000000.}
    # Set JPY Withdraw and Deposit
    jpy_deposit  = 3000000
    jpy_withdraw = 0
    # Set Holds
    assets = {'JPY':0.0 + jpy_withdraw, 'BTC':0.5, 'BCH':3.0, 'ZAIF':50.5}

    # Initialize Controller
    default, value = setLastYear(last_holds, last_price)
    controller = TotalController(default)
    funds = jpy_deposit + value

    # Read JPY/USD, BTC/JPY, BCH/JPY
    jpy = JPY('../data/2017/jpy/USDJPY.csv', '../data/2017/jpy/btc-jpy-max.csv', '../data/2017/jpy/bch-jpy-max.csv')
    # Join JPY Data When Read History of Each Exchange
    # Read Trade History of Bitfinex
    bitfinex = BitFinex('../data/2017/bitfinex/trades.csv', jpy)
    # Read Trade History of Cryptopia
    cryptopia = Cryptopia('../data/2017/cryptopia/trade.csv', jpy)
    # Read Trade History of Bitflyer
    bitflyer = BitFlyer('../data/2017/bitflyer/trade.csv', jpy)
    # Read Trade History of Zaif
    zaif = Zaif('../data/2017/zaif/trade.csv', jpy)

    # Calculate All Total
    exchanges = [bitfinex, cryptopia, bitflyer, zaif]
    for exchange in exchanges:
        controller = exchange.calcTotal(controller)
    # Print Summary
    controller.printSummary()
    # Calculate Profit
    print('Profit :', controller.calcProfit(funds, assets))


if __name__ == '__main__':
    main()
