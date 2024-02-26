import numpy as np
import pandas as pd
import yfinance as yf
class RawData:
    """
    A data class that take in raw data for preprocessing, cleaning
    """
    def __init__(self, ticker, start_date, end_date, interval):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        

    def load_data(self):
        self.df_price = yf.download(self.ticker, self.start_date, self.end_date, self.interval)
        return self.df_price


d = RawData('AAPL', "2010-10-10", "2015-10-10", "1d")
print(d.load_data())