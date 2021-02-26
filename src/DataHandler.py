import config, websocket, requests, json
from abc import ABC, abstractmethod # Abstract class module for python.
import alpaca_trade_api as tradeapi

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
        
    def submit_order(self): 
        pass

    @abstractmethod
    def get_bars(self, tickers, bar_timeframe, num_of_bars):
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
    def __init__(self,API_key_id,API_secret_key,base_url,socket = "wss://data.alpaca.markets/stream"):
        self.headers = {"APCA-API-KEY-ID":API_key_id, "APCA-API-SECRET-KEY":API_secret_key}
        self.base_url = base_url
        self.account_url= "{}/v2/account".format(self.base_url)
        self.order_url = "{}/v2/orders".format(self.base_url)
        self.api = tradeapi.REST(self.headers["APCA-API-KEY-ID"],self.headers["APCA-API-SECRET-KEY"],base_url)
        self.api_account = self.api.get_account()
        self.ws = websocket.WebSocketApp(socket, 
                    on_message = lambda msg: self.on_message(msg),
                    on_error   = lambda msg: self.on_error(msg),
                    on_close   = lambda:     self.on_close(),
                    on_open    = lambda:     self.on_open())
    
    def get_account(self):
        return self.api_account

    def set_account(self, account):
        self.acount = account

    def set_socket(self,socket = "wss://data.alpaca.markets/stream"):
        self.ws = websocket.WebSocketApp(socket, 
                    on_message = lambda msg: self.on_message(msg),
                    on_error   = lambda msg: self.on_error(msg),
                    on_close   = lambda:     self.on_close(),
                    on_open    = lambda:     self.on_open())
    def get_socket(self):
        return self.ws
        
    def submit_order(self,symbol, qty, side, type, time_in_force, limit_price=None, stop_price=None, 
                   client_order_id=None, order_class=None, take_profit=None, stop_loss=None, 
                   trail_price=None, trail_percent=None):
        self.api.submit_order(symbol, qty, side, type, time_in_force, limit_price, stop_price, 
                        client_order_id, order_class, take_profit, stop_loss, 
                        trail_price, trail_percent)
    
    def get_bars(self, tickers, bar_timeframe, num_of_bars):
        
        url = 'https://data.alpaca.markets/v1/bars'+'/'+bar_timeframe+'?symbols='+tickers+'&limit='+num_of_bars
        r = requests.get(url, headers=self.headers)
        print(json.dumps(r.json(), indent=4))

    
    def on_open(self):
        """
        function called whenever a websocket is opened, authenticates with alpaca
        """
        print("opened-stream")
        auth_data = {
            "action": "authenticate",
            "data": {"key_id": config.API_KEY, "secret_key": config.SECRET_KEY}
        }
        self.ws.send(json.dumps(auth_data))

    def on_message(self, message):
        print("received a message")
        print(message)

    def on_close(self):
        print("closed connection")

    def on_error(self, error):
        print(error)

    def listen(self,ticker,channel_name):
        """
        function that sends a listen message to alpaca for the streams inputed.
        """
        for x in range(ticker):
            ticker[x] = channel_name + ticker[x]

        listen_message = {"action": "listen", "data": {"streams": ticker}}
        self.ws.send(json.dumps(listen_message))

    def unlisten(self,ticker,channel_name):
        """
        
        function that unlistens for the streams inputed.
            might need error checking if a stream that is not currently being listened to is asked to be unlistened.
        """
        for x in range(ticker):
            ticker[x] = channel_name + ticker[x]
        unlisten_message = {"action": "unlisten", "data": {"streams": ticker}}
        self.ws.send(json.dumps(unlisten_message))