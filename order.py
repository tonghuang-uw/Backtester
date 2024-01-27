
class Order():
    """ Then a order is filled, we create a order object
    """
    def __init__(self, ticker, side, size, idx):
        self.ticker = ticker
        self.side = side
        self.size = size
        self.idx = idx
        self.type = "market"