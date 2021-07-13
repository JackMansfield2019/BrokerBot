import websocket
import requests
import json  # For web connectivity
from abc import ABC, abstractmethod  # Abstract class module for python.
import alpaca_trade_api as tradeapi
from dataclasses import dataclass  # Python structs module.
import pandas as pd  # For data storage and analysis.
import ast, datetime # For on_message data handling
"""
overview:
    - DataHandler Class: DataHandler is a class that takes in data from a given brokerage API,
      and sends it through to the StrategyHandler in a format that it can natively understand.
      in short, it is responsible for data transfer and formatting.

    - Standard Data Format (BBFrame): BBFrame is the standard data format used in the BrokerBot
      project. it consists of a Pandas dataframe in the following configuration:
            ================================================================
            |      |  Time  |  Open  |  High  |  Low  |  Close  |  Volume  | <- Labelled columns
            |  01  | string |  float |  float | float |  float  |   float  | 
            |  02  | string |  float |  float | float |  float  |   float  | 
            ================================================================
               ^^
               auto-numbered rows (see pandas Dataframe for more info.)

TODO: 
    - More concretely define abstract methods for base class.
    - Support more API subclasses.
    -  
"""


class DataHandler(ABC):
    # ==================== Creators ====================

    # ==================== Observers ===================
    """
    requires: nothing.
    modifies: nothing.
    effects:  nothing.
    returns:  an account object for the API.
    """
    @abstractmethod
    def get_account(self):
        pass
    """
    requires: nothing.
    modifies: nothing.
    effects:  nothing.
    returns:  the socket object for the API.
    """
    @abstractmethod
    def get_socket(self):
        pass

# ==================== Producers ===================

    """
    requires: ticker for given stock, start time for bar data, end time of bar data, and length of bar.
    modifies: nothing.
    effects:  nothing.
    returns:  a Pandas Dataframe containing the bars data in BrokerBot Standard Format (BBFrame).
    """
    @abstractmethod
    def get_bars(self, tickers, bar_timeframe, num_of_bars):
        pass


# ==================== Mutators ====================
    """
    requires: The new account to set this one to.
    modifies: The current account object, replacing it with the argument account.
    effects:  nothing.
    returns:  nothing.
    """
    @abstractmethod
    def set_account(self, account):
        pass


# ===================== Misc =======================

    @abstractmethod
    def on_open(self):
        pass

    @abstractmethod
    def on_message(self):
        pass

    @abstractmethod
    def on_close(self):
        pass

    @abstractmethod
    def on_error(self):
        pass

    @abstractmethod
    def listen(self):
        pass

    @abstractmethod
    def unlisten(self):
        pass


class AlpacaDataHandler(DataHandler):
    def __init__(self,
                 api_key,
                 secret_key,
                 base_url,
                 socket="ws://data.alpaca.markets/stream"):
        self.api_key = api_key
        self.secret_key = secret_key
        self.headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": secret_key
        }
        self.base_url = base_url
        self.account_url = "{}/v2/account".format(self.base_url)
        self.order_url = "{}/v2/orders".format(self.base_url)
        self.api = tradeapi.REST(self.headers["APCA-API-KEY-ID"],
                                 self.headers["APCA-API-SECRET-KEY"], base_url)
        self.api_account = self.api.get_account()
        self.ws = None
        self.socket = socket
        self.pending_tickers = []
        self.sh_queue = None

    def set_sh_queue(self, q):
        self.sh_queue = q

    def get_account(self):
        return self.api_account

    def set_account(self, account):
        self.acount = account

    def get_socket(self):
        return self.ws


    """
    requires: Strings for the ticker, start and end time in RFC-3339 format(e.g. 2021-03-11T00:00:00-05:00), 
              timeframe (currently only '1Day', '1Hour', and '1Min'), 
              and bar_limit, which limits the number of bars returned within that timeframe.
    modifies: nothing.
    effects:  nothing.
    returns:  A Pandas Dataframe containing the bars data. 
    """
    def get_bars(self, ticker: str, start_time: str, end_time: str, bar_timeframe: str, bar_limit: str):
        url ='https://data.alpaca.markets/v2/stocks'+'/'+ticker+'/bars?adjustment=raw'+'&start='+start_time+'&end='+end_time+'&limit='+bar_limit+'&page_token='+'&timeframe='+bar_timeframe
        r = requests.get(url, headers=self.headers)
        df = pd.read_json(json.dumps(r.json()['bars']))
        df['oi'] = -1
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Open Interest']
        print(df)
        return df

    # Socket Functions

    def on_open(self, ws):
        print("on open")

        # function called whenever a websocket is opened, authenticates with alpaca

        auth_data = {
            "action": "authenticate",
            "data": {
                "key_id": self.api_key,
                "secret_key": self.secret_key
            }
        }
        ws.send(json.dumps(auth_data))
        print("sent auth")
        listen_message = {
            "action": "listen",
            "data": {
                "streams": [f"AM.{self.pending_tickers.pop()}", "AM.GME"]
            }
        }
        # check pending tickers, sne initial listen message, wait for new tickers,
        ws.send(json.dumps(listen_message))

    """
    requires: Reference to the WebSocketApp and the message that was receieved.
    modifies: nothing.
    effects:  Sends a DataFrame to SH via the pipe.
    returns:  nothing.
    """

    def on_message(self, ws, message):
        print("received a message")
        print(message)
        # convert message to dictionary
        message = ast.literal_eval(message)
        # message is not an authorization or listening message, so it must be a minute bars message
        if message["stream"] != "authorization" and message["stream"] != "listening":
            timestamp = datetime.datetime.fromtimestamp(message["data"]["e"] / 1000)
            timestamp = timestamp.isoformat("T")
            op = message["data"]["o"]
            high = message["data"]["h"]
            low = message["data"]["l"]
            cl = message["data"]["c"]
            vol = message["data"]["v"]
            data = [[timestamp, op, high, low, cl, vol]]
            df = pd.DataFrame(data, columns=["Time", "Open", "High", "Low", "Close", "Volume"])
            self.sh_queue.put(df)

    def on_close(self, ws):
        print("closed connection")

    def on_error(self, ws, error):
        print(error)

    def start_streaming(self, tickers):
        self.pending_tickers += tickers
        print(self.socket)
        self.ws = websocket.WebSocketApp(
            self.socket,
            on_message=lambda ws, msg: self.on_message(self.ws, msg),
            on_close=lambda ws: self.on_close(self.ws),
            on_open=lambda ws: self.on_open(self.ws),
            on_error=lambda ws, error: self.on_error(self.ws, error))

        self.ws.run_forever()
        print("HELLO")

    def listen(self, tickers, channel_name):
        #
        # function that sends a listen message to alpaca for the streams inputed.
        #
        for x in range(len(tickers)):
            tickers[x] = channel_name + "." + tickers[x]
        print(tickers)
        listen_message = {"action": "listen", "data": {"streams": tickers}}
        self.ws.send(json.dumps(listen_message))
        #self.stream_conn.run(quote_callback, tickers)

    def unlisten(self, ticker, channel_name):
        #
        # function that unlistens for the streams inputed.
        #     might need error checking if a stream that is not currently being listened to is asked to be unlistened.
        #
        for x in range(ticker):
            ticker[x] = channel_name + ticker[x]
        unlisten_message = {"action": "unlisten", "data": {"streams": ticker}}
        self.ws.send(json.dumps(unlisten_message))
