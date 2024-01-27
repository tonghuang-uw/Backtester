
from order import Order
from trade import Trade

class Strategy():
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