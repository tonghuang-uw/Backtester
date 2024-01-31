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
    
    def _get_trade(self):
        # return index, side, size, price
        return self.idx, self.side, self.size, self.price

    def __repr__(self):
        return f'<Trade: {self.idx} {self.side} {self.ticker} {self.size} @ {self.price}'

