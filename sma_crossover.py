import pandas as pd
import numpy as np
from Strategy import Strategy

class sma_crossover(Strategy):

    def __init__(self, slow, fast):
        """
        slow: int, the slow moving average
        fast: int, the fast moving average
        """
        super().__init__()

        # initiate ma data
        self.ma_data = self.data

        self.slow = slow
        self.fast = fast

        # automatically calculate the moving average
        self.calculate_ma()

    def calculate_ma(self):
        self.ma_data[f'sma_{self.slow}'] = self.ma_data['Close'].rolling(self.slow).mean()
        self.ma_data[f'sma_{self.fast}'] = self.ma_data['Close'].rolling(self.fast).mean()
    def on_bar(self):
        fast_ma = self.ma_data.loc[self.current_idx][f'sma_{self.fast}']
        slow_ma = self.ma_data.loc[self.current_idx][f'sna_{self.slow}']
        
        if self.position_size == 0:
            