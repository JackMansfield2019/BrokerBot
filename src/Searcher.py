import config
import websocket, json
import numpy as np 
import pandas as pd
import requests
import math
import alpaca_trade_api as tradeapi 
import time # used for calculating time 
from statistics import mean # used to calculate avg volume 

class Searcher:
  def __init__(self,API_key_id,API_secret_key,base_url,socket = "wss://data.alpaca.markets/stream"):
  	
  	self.headers = {"APCA-API-KEY-ID":API_key_id, "APCA-API-SECRET-KEY":API_secret_key}
    self.base_url = base_url
    self.account_url= "{}/v2/account".format(self.base_url)
    self.order_url = "{}/v2/orders".format(self.base_url)
    self.api = tradeapi.REST(
                          headers[APCA-API-KEY-ID],
                          headers[APCA-API-SECRET-KEY],
                          base_url
          )
    self.api_account = api.get_account()
    self.socket = socket
    self.stocks = pd.read_csv('S&P500-Symbols.csv')
    Columns = ['Ticker', 'Time', 'Volume']
    self.dataframe = pd.DataFrame(columns = Columns) 
    self.stock_data = dataframe.set_index("Ticker", drop = False) 

    #sets the time for each stock to the time we first initialize the searcher. 
    for stock in self.stocks:
      t = int(time.time())
      self.stock_data = self.stock_data.append( pd.Series([ stock, t], index = cols ), ignore_index = True) 

  def get_account(self):
    return account

  '''
    Overview: loops through each stock in the S&P-500, builds a dataframe of equal-weighted volume of stocks in the S&P500, then returns a decision***

    Requires: none
    Modifies: none
    Effects: none
    Returns: *** 

    At Present: Creates the unweighted S&P500 of the stocks' volumes
    To Do: Figure out what volume calculation to use, so select stock and add it to the priority queue. 
  '''
  def search(self):
    Volumes = []
    for stock in self.stocks and time_initial in self.stock_data.items():
        time_final, average_volume = self.get_data(stock, time_initial) 
        Volumes.append(average_volume)
        stock_data.at[stock, 'Time'] = time_final # updates the stock's time cell 
        stock_data.at[stock, 'Volume'] = average_volume # updates the stock's volume cell 

        #looking at top 5 stocks
        best = [] 

        # Puts the top 5 changes in volume into best loop 
        for volume in Volumes:
          if len(best) < 5:
             best.append(volume) 
          else:
            if vol > min(best):
              best.remove(min(best))
              best.append(volume)

        
        best_stocks = [] # Appends the respective stock tickers of the volumes in best list. 
        for volume in best:
          for stock in self.stocks:
            if volume == self.stock_data.iloc(stock, "Volume"):
              best_stocks.append(stock) 
        
        return best_stocks # returns the top 5 stocks to look at due to their biggest change in average volume 


  '''
    Overview: returns the previous 5-minute-volume for the given stock by the client 

    Requires: stock is not null
    Modifies: none
    Effects: none
    Returns: volume of the stock that was passed in 

    Question: How many tickers are we limited to per API request? Answer: 200 
    sockets limited to 30 

  '''
  def get_data(self, stock, time_initial):
    # stock refers to the stock passed in
    # 5Min refers to the timeframe
    # limit=5 refers to how many bars back we take the volume 
    # time frame within the day 

    # gets seconds elapsed, because the time is in Unix Epoch 
    # subtracts current time with the stock's previous end-time
    time_elapsed = int(time.time()) - time_initial

    # finds how many 5-minute bars have passed since time_initial (timeIn) 
    bars = time_elapsed/300 

    barset = api.get_barset(stock, '5Min', limit=bars)
    #stock_bar = barset[stock]
    
    #assuming the previous bar from current is in the last index of barset 
    last = len(barset) - 1 
    stock_time = barset[last][0]

    # stock_vols contains the volume of each bar of the stock 
    stock_volumes = []
    for i in range(0, len(barset)):
      stock_volumes.append(barset[i][5]) #appends the volume of each bar in barset to the stock_vol list 
    
    # calculates the mean of the stock volumes 
    stock_average_volume = int(mean(stock_volumes)) 
    return stock_time, stock_average_volume 

# *** gets the data from the broker bot priority queue ***

  def set_socket(self,socket = "wss://data.alpaca.markets/stream"):
    self.socket = socket

  def submit_order(self,symbol, qty, side, type, time_in_force, limit_price=None, stop_price=None, 
                   client_order_id=None, order_class=None, take_profit=None, stop_loss=None, 
                   trail_price=None, trail_percent=None):
    
    api.submit_order(symbol, qty, side, type, time_in_force, limit_price, stop_price, 
                   client_order_id, order_class, take_profit, stop_loss, 
                   trail_price, trail_percent)

  def on_open():
      print("opened-stream")
      auth_data = {
          "action": "authenticate",
          "data": {"key_id": config.API_KEY, "secret_key": config.SECRET_KEY}
      }

      ws.send(json.dumps(auth_data))

      listen_message = {"action": "listen", "data": {"streams": ["AM.TSLA"]}}

      ws.send(json.dumps(listen_message))


  def on_message(ws, message):
      print("received a message")
      print(message)

  def on_close(ws):
      print("closed connection")

  socket = "wss://data.alpaca.markets/stream"

  ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
  ws.run_forever()