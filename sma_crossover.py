import pandas as pd
import numpy as np
from Strategy import Strategy

class sma_crossover(Strategy):

    def __init__(self, data, slow, fast):
        """
        slow: int, the slow moving average
        fast: int, the fast moving average
        """
        super().__init__()

        # initiate ma data
        self.ma_data = data

        self.slow = slow
        self.fast = fast
    
    def calculate_ma(self):
        self.ma_data[f'sma_{self.slow}'] = self.ma_data['price'].rolling(self.slow).mean()
        self.ma_data[f'sma_{self.fast}'] = self.ma_data['price'].rolling(self.fast).mean()
    
data = pd.DataFrame({
    'price': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
})

# Instantiate your class
sma_test = sma_crossover(data=data, slow=3, fast=2)

# Calculate moving averages
sma_test.calculate_ma()

# Verify the output
print(sma_test.ma_data)