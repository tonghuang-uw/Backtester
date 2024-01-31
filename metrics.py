import numpy as np
import pandas as pd


class metricsCalculator():
    "Calculate the metrics of a trading strategy"
    def __init__(self, total_assets, total_cash, trades = None):
        """
        total_assets: dict,
        total_cash: dict
        """
        # make a dataframe for the asset position and cash position
        self.df = pd.DataFrame.from_dict({'assets': total_assets, 'cash': total_cash})
        self.df['total_aum'] = self.df['assets'] + self.df['cash']
        self.p = self.df['total_aum']
        self.trades = trades

    def calculate_total_return(self):
        # Calculate the total return of the strategy
        total_return = self.p.iloc[-1]/self.p.iloc[0] - 1
        
        return total_return

    def calculate_annualized_return(self):
        # Calculate the annualized return of the strategy
        annualized_return = (self.p.iloc[-1]/self.p.iloc[0])**((1 / (self.p.index[-1] - self.p.index[0]).days / 252))
        return annualized_return

    def calculate_standard_deviation(self):
        # Calculate the annualized standard deviation of the strategy (volatility)
        standard_deviation = self.p.pct_change().std() * np.sqrt(252)
        return standard_deviation
    
    def calculate_sharpe_ratio(self, rf=0.0):
        # Calculate the sharpe ratio of the strategy
        annualized_return = (self.p.iloc[-1]/self.p.iloc[0])**((1 / (self.p.index[-1] - self.p.index[0]).days / 252))
        standard_deviation = self.p.pct_change().std() * np.sqrt(252)

        sharpe_ratio = (annualized_return - rf)/standard_deviation
        return sharpe_ratio
    
    def calculate_maximum_drawdown(self):
        # Calculate the maximum drawdown of the strategy
        peak_value = self.p[0]
        previous_value = self.p[0]
        max_drawdown = 0

        for value in self.p:
            # update the peak
            if value > peak_value:
                peak_value = value
            
            # calculate the drawdown of the current peak
            drawdown = (peak_value - value)/peak_value

            # update max_drawdown
            if drawdown > max_drawdown:
                max_drawdown = drawdown

        return max_drawdown
        

    def calculate_win_loss_ratio(self):
        # calculate the winning and lossing ratio of the strategy

        for trade in self.trades:
            idx, side, size, price = trade._get_trade()
            print(idx, side, size, price)



    
    