# -*- coding: utf-8 -*-
from jpy import JPY
from bitfinex import BitFinex
from cryptopia import Cryptopia
from bitflyer import BitFlyer
from zaif import Zaif
from controller import Controller


def main():
    # Set Holds
    holds = {'BTC':0.5, 'BCH':3.0, 'ZAIF':50.5}
    # Read JPY/USD, BTC/JPY, BCH/JPY
    jpy = JPY('../data/2017/jpy/USDJPY.csv', '../data/2017/jpy/btc-jpy-max.csv', '../data/2017/jpy/bch-jpy-max.csv')
    # Join JPY Data When Read History of Each Exchange
    # Read Trade (and Withdraw) History of Bitfinex
    bitfinex = BitFinex('bitfinex', '../data/2017/bitfinex/trades.csv', jpy)
    # Read Trade (and Withdraw) History of Cryptopia
    cryptopia = Cryptopia('cryptopia', '../data/2017/cryptopia/trade.csv', '../data/2017/cryptopia/withdraw.csv', jpy)
    # Read Trade (and Withdraw) History of Bitflyer
    bitflyer = BitFlyer('bitflyer', '../data/2017/bitflyer/trade.csv', '../data/2017/bitflyer/withdraw.csv', jpy)
    # Read Trade (and Withdraw) History of Zaif
    zaif = Zaif('zaif', '../data/2017/zaif/trade.csv', '../data/2017/zaif/withdraw.csv', jpy)
    # Init Controller
    controller = Controller([bitfinex, cryptopia, bitflyer, zaif])
    # Calculate Result of Each Exchange
    print('format : 通貨 (売却額 - 購入額, 売却数, 購入数, 売却額総平均, 購入額総平均')
    controller.calcExchangeResult()
    # controller.printExchangeSummary()
    # Calculate Result of Currencies
    controller.calcTotalExchangeResult()
    controller.printTotalExchangeSummary()
    # Calculate Total
    print('Profit :', controller.calcProfit(holds))


if __name__ == '__main__':
    main()
