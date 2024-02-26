from Strategy import Strategy

class BuyAndSellSwitch(Strategy):
    def __init__(self):
        super().__init__()
    def on_bar(self):
        if self.position_size == 0:
            self.buy('AAPL', 1)
            print(self.current_idx,"buy")
        else:
            self.sell('AAPL', 1)
            print(self.position_size)
            print(self.current_idx,"sell")
            
