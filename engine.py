import pandas as pd
from tqdm import tqdm
import yfinance as yf
from Strategy import Strategy
from order import Order
from trade import Trade
from list_strategy import BuyAndSellSwitch

class Engine():
    """ The engine class is the main object to be used for backtest
    """
    def __init__(self, starting_account = 50000):
        self.strategy = None
        self.data = None
        self.cash = starting_account
        self.current_idx = None
    
    def add_data(self, data):
        self.data = data

    def add_strategy(self, strategy):
        self.strategy = strategy

    def run(self):
        self.strategy.data = self.data

        for idx in tqdm(self.data.index):
            self.current_idx = idx
            self.strategy.current_idx = self.current_idx

            self._fill_orders()

            self.strategy.on_bar()
            print(idx)
    def _fill_orders(self):
        """ this method fill buy and sell orders, create a trade object and adjust cash amount
        """
        for order in self.strategy.orders:
            can_fill = False
            if order.side == 'buy' and self.cash >= self.data.loc[self.current_idx]['Open'] * order.size:
                can_fill = True
            elif order.side == 'sell' and self.strategy.position_size >= order.size:
                can_fill = True
            if can_fill:
                t = Trade(
                    ticker = order.ticker,
                    side = order.side,
                    size = order.size,
                    idx = order.idx,
                    type = order.type,
                    price = self.data.loc[self.current_idx]['Open']
                )
            self.strategy.trades.append(t)
            self.cash -= t.price * t.size
        self.strategy.orders = []



strategy = BuyAndSellSwitch()
data = yf.Ticker('AAPL').history(start='2020-01-01', end='2022-12-31', interval='1d')
e = Engine()
e.add_data(data)
e.add_strategy(strategy)
e.run()
print(e.strategy.trades)
