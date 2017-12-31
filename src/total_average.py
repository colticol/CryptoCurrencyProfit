# -*- coding: utf-8 -*-
from jpy import JPY
from bitfinex import BitFinex
from cryptopia import Cryptopia
from bitflyer import BitFlyer
from zaif import Zaif
from controller import Controller


def main():
    # Set Holds
    holds = {'BTC':0.0001, 'BCH':45.37983532, 'ZAIF':2154694.4}
    # Read JPY/USD, BTC/JPY, BCH/JPY
    jpy = JPY('../data/2017/jpy/USDJPY.csv', '../data/2017/jpy/btc-jpy-max.csv', '../data/2017/jpy/bch-jpy-max.csv')
    # Join JPY Data When Read History of Each Exchange
    # Read Trade (and Withdraw) History of Bitfinex
    bitfinex = BitFinex('bitfinex', '../data/2017/bitfinex/2017-12-28-trades.csv', jpy)
    # Read Trade (and Withdraw) History of Cryptopia
    cryptopia = Cryptopia('cryptopia', '../data/2017/cryptopia/Trade_History.csv', '../data/2017/cryptopia/Withdraw_History.csv', jpy)
    # Read Trade (and Withdraw) History of Bitflyer
    bitflyer = BitFlyer('bitflyer', '../data/2017/bitflyer/TradeHistory_20171228.csv', '../data/2017/bitflyer/Deposit_Withdraw_History_20171228.csv', jpy)
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
