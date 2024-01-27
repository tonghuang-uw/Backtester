class Trade():
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