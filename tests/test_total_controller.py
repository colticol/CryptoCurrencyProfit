from unittest import TestCase
import sys
sys.path.append('src/')
from total_controller import TotalController


class TestTotalController(TestCase):

    def testCalcProfit(self):
        # init
        funds = 1000000
        controller = TotalController({})
        # buy 0.5BTC for 500000 yen
        # 1BTC = 1000000 yen
        controller.buy('BTC', 500000, 0.5)
        controller.sell('JPY', 500000, 500000)
        # buy 1.0BCH for 100000 yen
        # 1BCH = 100000 yen
        controller.buy('BCH', 100000, 1.0)
        controller.sell('JPY', 100000, 100000)
        # sell 0.2BTC for 0.1BCH
        # 1BTC = 100000 yen, 1BCH = 200000 yen
        controller.sell('BTC', 20000, 0.2)
        controller.buy('BCH', 20000, 0.1)
        # sell 0.5BCH for 200000 yen
        # 1BCH = 400000 yen
        controller.sell('BCH', 200000, 0.5)
        controller.buy('JPY', 200000, 200000)
        # assets
        assets = {'JPY':600000, 'BTC':0.3, 'BCH':0.6}
        # profit
        profit = controller.calcProfit(funds, assets)
        self.assertAlmostEqual(profit, -34545.454545, places=5)
