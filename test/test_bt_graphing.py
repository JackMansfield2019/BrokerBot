'''
Backtrader Plotting - example taken from API docs and modified
- takes in data from...
     * GenericCSVData *
    VisualChartCSVData
    YahooFinanceData (for online downloads)
    * YahooFinanceCSVData (for already downloaded data) *
    BacktraderCSVData (in-house … for testing purposed, but can be used)
    
    YahooFinanceCSVData has similar format to our DH, cols are
    Date    Open    High    Low    Close    Adj Close    Volume
    
- essentially combines backtrader with matplotlib to make it easier to plot
  strategies and results
- can use a number of technical indicators through bt.Strategy, not sure how this would
  integrate with our classes
  
'''

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt


class St(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data)


data = bt.feeds.YahooFinanceCSVData(dataname='data/AAPL.csv')

cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(St)
cerebro.run()
cerebro.plot()
