import websocket
import requests
import json
from abc import ABC, abstractmethod  # Abstract class module for python.
from alpaca_trade_api import StreamConn
import alpaca_trade_api as tradeapi  # pip


# Imports for testing various data structures, most will be removed soon.
from dataclasses import dataclass  # Allows for struct-like classes in python.
from numpy import array as np_array
from timeit import Timer
from typing import NamedTuple
# from pandas import DataFrame as df
import pandas as pd


# Data format using a dataclass, one option for storage, may be heavy though.
@dataclass
class OOPBar:
    __slots__ = ['time', 'open', 'high', 'low', 'close']
    time: str   # Time in RFC339 format
    open: float   # Opening price
    high: float   # High price
    low: float   # Low Price
    close: float   # Closing price

# Data format using a NamedTuple, is immutable but still may be heavy.


class ImmutableBar(NamedTuple):
    time: str   # Time in RFC339 format
    open: float   # Opening price
    high: float   # High price
    low: float   # Low Price
    close: float   # Closing price

# Pandas Dataframe, a library used for python datascience, akin to a 2D table in Excel
# 2D Numpy Array: a 2d array of these values used for quick iteration speed and minimal bloat.


# Abstract base class for the data handler, to facilitate different apis using subclasses.
class DataHandler(ABC):
    @abstractmethod
    def get_account(self):
        pass

    @abstractmethod
    def set_account(self, account):
        pass

    def set_socket(self):
        pass

    def get_socket(self):
        pass

    @abstractmethod
    def get_bars_OOP(self, tickers, bar_timeframe, num_of_bars):
        pass

    def on_open(self):
        pass

    def on_message(self):
        pass

    def on_close(self):
        pass

    def on_error(self):
        pass

    def listen(self):
        pass

    def unlisten(self):
        pass


class AlpacaDataHandler(DataHandler):
    def __init__(self, API_key_id, API_secret_key, base_url, data_url, socket="wss://data.alpaca.markets/stream"):
        self.headers = {"APCA-API-KEY-ID": API_key_id,
                        "APCA-API-SECRET-KEY": API_secret_key}
        self.base_url = base_url
        self.account_url = "{}/v2/account".format(self.base_url)
        self.order_url = "{}/v2/orders".format(self.base_url)
        self.api = tradeapi.REST(
            self.headers["APCA-API-KEY-ID"], self.headers["APCA-API-SECRET-KEY"], base_url)
        self.api_account = self.api.get_account()

        """
        self.stream_conn = StreamConn(
            API_key_id,
            API_secret_key,
            base_url=base_url,
            data_url=data_url
        )
        """"

        """
        print("socket: "+ socket)
        self.ws = websocket.WebSocketApp(socket,
                                         on_message=lambda msg: self.on_message(
                                             msg),
                                         on_error=lambda msg: self.on_error(
                                             msg),
                                         on_close=lambda:     self.on_close(),
                                         on_open=lambda:     self.on_open())
        """"
    
    """"
    @self.stream_conn.on(r'^AM\..+$')
    async def on_minute_bars(conn, channel, bar):
        print('bars', bar)

    @conn.on(r'Q\..+')
    async def on_quotes(conn, channel, quote):
        print('quote', quote)

    @conn.on(r'T\..+')
    async def on_trades(conn, channel, trade):
        print('trade', trade)
    """"
    def get_account(self):
        return self.api_account

    def set_account(self, account):
        self.acount = account

    def get_socket(self):
        return self.ws

    def get_bars_OOP(self, tickers, bar_timeframe, num_of_bars):

        url = 'https://data.alpaca.markets/v1/bars'+'/' + \
            bar_timeframe+'?symbols='+tickers+'&limit='+num_of_bars
        r = requests.get(url, headers=self.headers)
        dict = json.dumps(r.json(), indent=4)
        x = len(dict)/5
        arr = np_array(x)
        for i in x:
            arr[i] = OOPBar()
            arr[i].time = dict[((i+1)*5)-5]
            arr[i].open = dict[((i+1)*5)-4]
            arr[i].high = dict[((i+1)*5)-3]
            arr[i].low = dict[((i+1)*5)-2]
            arr[i].close = dict[((i+1)*5)-1]
        return arr

    def get_bars_pandas(self, tickers, bar_timeframe, num_of_bars):

        url = 'https://data.alpaca.markets/v1/bars'+'/' + \
            bar_timeframe+'?symbols='+tickers+'&limit='+num_of_bars
        r = requests.get(url, headers=self.headers)
        df = pd.read_json(r.json())
        return df

    def on_open(self):
        """
        function called whenever a websocket is opened, authenticates with alpaca
        """
        """
        print("opened-stream")
        auth_data = {
            "action": "authenticate",
            "data": {"key_id": config.API_KEY, "secret_key": config.SECRET_KEY}
        }
        self.ws.send(json.dumps(auth_data))
        listen_message = {"action": "listen", "data": {"streams": ["T.TSLA"]}}
        self.ws.send(json.dumps(listen_message))
        self.ws.run_forever()
        """

    def on_message(self, message):
        print("received a message")
        print(message)

    def on_close(self):
        print("closed connection")

    def on_error(self, error):
        print(error)

    def run_socket(self):
        self.ws.run_forever()
    
    def listen(self, tickers, channel_name):
        """
        function that sends a listen message to alpaca for the streams inputed.
        """
        for x in range (len(tickers)):
            tickers[x] = channel_name + "." + tickers[x]
        print(tickers)
        listen_message = {"action": "listen", "data": {"streams": tickers}}
        self.ws.send(json.dumps(listen_message))
        #self.stream_conn.run(quote_callback, tickers)

    def unlisten(self, ticker, channel_name):
        """
        function that unlistens for the streams inputed.
            might need error checking if a stream that is not currently being listened to is asked to be unlistened.
        """
        for x in range(ticker):
            ticker[x] = channel_name + ticker[x]
        unlisten_message = {"action": "unlisten", "data": {"streams": ticker}}
        self.ws.send(json.dumps(unlisten_message))

    def set_socket(self, socket="wss://data.alpaca.markets/stream"):
        print("socket: " + socket)
        self.ws = websocket.WebSocketApp(socket,
                                         on_message=lambda msg: self.on_message(
                                             msg),
                                         on_error=lambda msg: self.on_error(
                                             msg),
                                         on_close=lambda:     self.on_close(),
                                         on_open=lambda:     self.on_open())
        print("opened-stream")
        auth_data = {
            "action": "authenticate",
            "data": {"key_id": config.API_KEY, "secret_key": config.SECRET_KEY}
        }
        self.ws.send(json.dumps(auth_data))
        listen_message = {"action": "listen", "data": {"streams": ["T.TSLA"]}}
        self.ws.send(json.dumps(listen_message))
        self.ws.run_forever()