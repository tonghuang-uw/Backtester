import pandas as pd
from tqdm import tqdm
import yfinance as yf
class Engine:
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

class Strategy:
    """ The strategy class is the object to add strategy to the engine
    """
    def __init__(self):
        self.current_idx = None
        self.data = None
        self.orders = []
        self.trades = []

    def buy(self, ticker, size = 1):
        self.orders.append(
            Order(
                ticker = ticker,
                side = 'buy',
                size = size,
                idx = self.current_idx
            )
        )
    
    def sell(self, ticker, size = 1):
        self.orders.append(
            Order(
                ticker = ticker,
                side = 'sell',
                size = -size,
                idx = self.current_idx
            )
        )
    
    
    @property
    def position_size(self):
        return sum([t.size for t in self.trades])

class Trade:
    """ The trade object is created when a trade is created
    """
    def __init__(self, ticker, side, price, size, idx, type):
        self.ticker = ticker
        self.side = side
        self.size = size
        self.idx = idx
        self.type = type
        self.price = price
    
    def __repr__(self):
        return f'<Trade: {self.idx} {self.ticker} {self.size} @ {self.price}'

class Order:
    """ Then a order is filled, we create a order object
    """
    def __init__(self, ticker, side, size, idx):
        self.ticker = ticker
        self.side = side
        self.size = size
        self.idx = idx
        self.type = "market"

class BuyAndSellSwitch(Strategy):
    def on_bar(self):
        if self.position_size == 0:
            self.buy('AAPL', 1)
            print(self.current_idx,"buy")
        else:
            self.sell('AAPL', 1)
            print(self.position_size)
            print(self.current_idx,"sell")

strategy = BuyAndSellSwitch()
data = yf.Ticker('AAPL').history(start='2020-01-01', end='2022-12-31', interval='1d')
e = Engine()
e.add_data(data)
e.add_strategy(strategy)
e.run()
print(e.strategy.trades)
