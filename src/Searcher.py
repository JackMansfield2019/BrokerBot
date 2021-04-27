import websocket
import json
import numpy as np
import pandas as pd
import requests
import math
import alpaca_trade_api as tradeapi
import time  # used for calculating time
from statistics import mean  # used to calculate avg volume

class TimeFrame(Enum):
  ONE_MIN = "1Min"
  FIVE_MIN = "5Min"
  FIFTEEN_MIN = "15Min"
  ONE_HOUR = "1Hour"
  ONE_DAY = "1Day"

class Searcher:
  def __init__(self, API_key_id, API_secret_key, base_url, socket, strat_conns):
    self.headers = {"APCA-API-KEY-ID": API_key_id,"APCA-API-SECRET-KEY": API_secret_key}
    self.base_url = base_url
    self.account_url= "{}/v2/account".format(self.base_url)
    self.order_url = "{}/v2/orders".format(self.base_url)
    self.strat_conns = strat_conns
    self.strat_counter = 0
    self.stock_set = set()
    self.api = tradeapi.REST(
                          self.headers["APCA-API-KEY-ID"],
                          self.headers["APCA-API-SECRET-KEY"],
                          base_url
          )
    # self.api_account = api.get_account()
    self.socket = socket
    self.DH = AlpacaDataHandler(API_key_id, API_secret_key, base_url) 

    """
    Columns = ['Ticker', 'Time', 'Volume']
    self.dataframe = pd.DataFrame(columns = Columns) 
    self.stock_data = dataframe.set_index("Ticker", drop = False) 

    # sets the time for each stock to the time we first initialize the searcher. 
    for stock in self.stocks:
      t = int(time.time())
      self.stock_data = self.stock_data.append( pd.Series([ stock, t], index = cols ), ignore_index = True) 
    """
    self.stocks = pd.read_csv("files/Symbols.csv")
    time = int(time.time()) 
    stock_data = {}
    for stock in stocks:
      stock_data[stock] = time 
    #self.queue = [[]] # priority queue

  def get_account(self):
    return account

  """
    Overview: updates the priority of each stock, THIS IS THE RUN METHOD OF SCREENER 
    Effects: updates the weights of the priority queue's stocks 
  """
  def search(self):
    for stock in self.stocks:
      time_initial = stock_data[stock] 
      time_final, stock_volume = self.get_data(stock, time_initial, TimeFrame.FIVE_MIN) 
      stock_data[stock] = time_final 
      self.ACV(stock_volume, stock) 


  """
    Overview: returns the previous 5-minute-volume for the given stock by the client 
    Returns: volume of the stock that was passed in
    Throws:
      - Exception if time_initial < 0 
      - Exception if stock is None/Null 
    N.B.: Ticker Limit per API Request = 200 
  """
  def get_data(self, stock, time_initial, timeframe):
    if time_initial < 0: raise Exception("Time Initial cannot be < 0!")
    if stock is None or stock == "": raise Exception("stock cannot be None/Null or blank!")

    time_current = int(time.time())  
    bars = int((time_current - time_initial) / 300)
    barset = DH.get_bars(stock, time_initial, time_current, timeframe, bars)   
    
    #assuming the previous bar from current is in the last index of barset 
    #last = len(barset) - 1 
    #stock_time = barset[last][0]

    stock_volume = []
    row_count = barset.shape[0] 
    stock_time = time_current 
    for i in range(0, row_count):
      stock_close.append(barset.iloc[i, 5])
    return stock_time, stock_volume 
  

  """
    Overview: calculates the average change in volume 
    Requires: volumes is not None
    Returns: updated priorities of each stock in stocks list  
  """
  def ACV(self, volumes, stock):
    acv = int(mean(volumes)) 
    s = [acv, stock]
    length = len(self.queue) 

    if len(self.queue) == 0:
      self.queue.append(s) 
    else:
      for i in range(0,length):
        if s[0] > self.queue[i][0]:
          self.queue.insert(i, s) 
          break 
        elif s[0] < self.queue[i][0] and i == length - 1:
          self.queue.append(s)  

"""
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
"""