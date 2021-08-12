import websocket
import json
import numpy as np
import pandas as pd
import requests
import math
import alpaca_trade_api as tradeapi
import time  # used for calculating time
from statistics import mean  # used to calculate avg volume
from ENUMS import Enum
from DataHandler import AlpacaDataHandler
from threading import Thread
#==================================================================================================================

class TimeFrame(Enum):
  ONE_MIN = "1Min"
  FIVE_MIN = "5Min"
  FIFTEEN_MIN = "15Min"
  ONE_HOUR = "1Hour"
  ONE_DAY = "1Day"
#==================================================================================================================

class Searcher:
  def __init__(self, API_key_id, API_secret_key, base_url, socket, strat_conns):
    self.headers = {"APCA-API-KEY-ID": API_key_id,"APCA-API-SECRET-KEY": API_secret_key}
    self.base_url = base_url
    self.account_url= "{}/v2/account".format(self.base_url)
    self.order_url = "{}/v2/orders".format(self.base_url)
    self.strat_conns = strat_conns
    self.strat_counter = 0
    self.stock_set = set()
    print("These are the parameters of searcher:")
    print(API_key_id)
    print(API_secret_key)
    print(base_url)
    print(socket)
    print(strat_conns)
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
    self.self.stock_data = dataframe.set_index("Ticker", drop = False) 

    # sets the time for each stock to the time we first initialize the searcher. 
    for stock in self.stocks:
      t = int(time.time())
      self.self.stock_data = self.self.stock_data.append( pd.Series([ stock, t], index = cols ), ignore_index = True) 
    """
    # self.stocks = pd.read_csv("../files/Symbols.csv")
    self.stocks = ["GOOGL","FB","AMZN","MSFT","AAPL","TSLA","TSM","BABA","JPM","JNJ","WMT","BAC"]
    time_now = int(time.time()) 
    self.stock_data = {}
    for stock in self.stocks:
      self.stock_data[stock] = time 
    self.queue = [] # priority queue
  #--------------------------------------------------------------------------------------------------------------

  def get_account(self):
    return account
  #--------------------------------------------------------------------------------------------------------------

  def forward_stocks_from_queue(self):
        while True:
          if len(self.stocks) == 0:
            time.sleep(2)
          else:
            for stock in self.stocks:
    
              if stock not in self.stock_set:
                strat_conn = self.strat_conns[self.strat_counter]
                strat_conn.send(stock)
                self.stock_set.add(stock)
                if self.strat_counter + 1 <= len(self.strat_conns)-1:
                  self.strat_counter += 1
                else:
                  self.strat_counter = 0
  #--------------------------------------------------------------------------------------------------------------

  def search(self):
    '''
    Updates the priority of each stock
    '''
    forward_thread = Thread(target=self.forward_stocks_from_queue, args=())
    forward_thread.start()


    # for stock in self.stocks:
    #   time_initial = self.stock_data[stock]
    #   print(time_initial) 
    #   time_final, stock_volume = self.get_data(stock, time_initial, TimeFrame.FIVE_MIN) 
    #   self.stock_data[stock] = time_final 
    #   self.ACV(stock_volume, stock) 

    # for stock in self.stocks:
    #   self.queue.append([0, stock])
  #--------------------------------------------------------------------------------------------------------------

  def get_data(self, stock, time_initial, timeframe):
    '''
    Returns the previous 5-minute-volume for the given stock by the client

      Parameters:
        stock (str): a security from any type of market 
        time_initial (time object): the previous time the stock was looked at 
        timeframe (str): the timeframe of data retrieved from the data handler 
      
      Returns:
        stock_time (time object): the time when the stock was looked at after the method call
        stock_volume (float): volume of the stock from the parameter 
      
      Throws:
        Exception if time_initial < 0
        Exception if stock is None
      
      N.B.: Ticker Limit per API Request = 200 
    '''
    # if time_initial < time.localtime: raise Exception("Time Initial cannot be < 0!")
    if stock is None or stock == "": raise Exception("stock cannot be None/Null or blank!")

    time_current = time.time()  
    bars = int((time_current - time_initial.time()) / 300)
    # print(f"{stock} {time_initial} {time_current} {timeframe} {bars}")
    barset = self.DH.get_bars(stock, time_initial, time_current, "5Min", str(bars))   
    
    #assuming the previous bar from current is in the last index of barset 
    #last = len(barset) - 1 
    #stock_time = barset[last][0]

    stock_volume = []
    row_count = barset.shape[0] 
    stock_time = time_current 
    for i in range(0, row_count):
      stock_close.append(barset.iloc[i, 5])
    return stock_time, stock_volume 
  #--------------------------------------------------------------------------------------------------------------
  
  def ACV(self, volumes, stock):
    '''
    Calculates the average change in volume, and updates them into the queue 
      
      Parameters:
        volumes (list of floats): volumes of a stock !!(must not be none)!!
        stock (str): a stock 
    '''
    acv = int(mean(volumes)) 
    s = [acv, stock]
    print(s)
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
  #--------------------------------------------------------------------------------------------------------------

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
#==================================================================================================================