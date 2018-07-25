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
    last_holds = {'BCH':45.37983532, 'ZAIF':2154694.4}
    last_price = {'BCH':161904.61979921136, 'ZAIF':0.8154790926917522}
    # Set JPY Withdraw and Deposit
    jpy_deposit  = 0
    jpy_withdraw = 1450000
    # Set Holds
    assets = {'JPY':72068. + jpy_withdraw, 'BCH':43., 'ZAIF':500000}

    # Initialize Controller
    default, value = setLastYear(last_holds, last_price)
    controller = TotalController(default)
    funds = jpy_deposit + value

    # Read JPY/USD, BTC/JPY, BCH/JPY
    jpy = JPY('../data/2018/jpy/USDJPY.csv', '../data/2018/jpy/btc-jpy-max.csv', '../data/2018/jpy/bch-jpy-max.csv')
    # Join JPY Data When Read History of Each Exchange
    # Read Trade (and Withdraw) History of Zaif
    zaif = Zaif('../data/2018/zaif/trade.csv', jpy)

    # Calculate All Total
    exchanges = [zaif]
    for exchange in exchanges:
        controller = exchange.calcTotal(controller)
    # Print Summary
    controller.printSummary()
    # Calculate Profit
    print('Profit :', controller.calcProfit(funds, assets))


if __name__ == '__main__':
    main()
