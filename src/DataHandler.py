import config, websocket, requests, json # For web connectivity
from abc import ABC, abstractmethod # Abstract class module for python.
import alpaca_trade_api as tradeapi
from dataclasses import dataclass # Python structs module.
import pandas as pd # For data storage and analysis.


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
    def __init__(self,
                 api_key,
                 secret_key,
                 base_url,
                 data_url,
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

    

    def get_account(self):
        return self.api_account

    def set_account(self, account):
        self.acount = account

    def get_socket(self):
        return self.ws


    """
    requires: ticker for given stock, start time for bar data, end time of bar data, and length of bar.
    modifies: nothing.
    effects:  nothing.
    returns: a Pandas Dataframe containing the bars data in BrokerBot Standard Format.
    """
    def get_bars(self, ticker, start_time, end_time, bar_length):
        url = 'https://data.alpaca.markets/v2/stocks'+'/'+'?symbol='+ticker+'/bars'+'&start='+start_time+'&end='+end_time+'&timeframe='+bar_length
        r = requests.get(url, headers=self.headers)
        df = pd.read_json(r.json())
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

    def on_message(self, ws, message):
        print("received a message")
        print(message)

    def on_close(self, ws):
        print("closed connection")

    def on_error(self, ws, error):
        print(error)


    def start_streaming(self, ticker):
       
        self.pending_tickers.append(ticker)
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

   
