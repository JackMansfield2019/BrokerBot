import websocket
import requests
import json  # For web connectivity
from abc import ABC, abstractmethod  # Abstract class module for python.
import alpaca_trade_api as tradeapi
from dataclasses import dataclass  # Python structs module.
import pandas as pd  # For data storage and analysis.
import ast, datetime # For on_message data handling
#==================================================================================================================

class DataHandler(ABC):
    """
    Class: DataHandler

    .............................................................................................................

    Overview
    --------
    A class that takes in data from a given brokerage API, and sends it through to the Strategy Handler in a format that it can natively understand.
    In short, it is responsible for data transfer and formatting.

    .............................................................................................................

    Standard Data Fromat (BBFrame)
    ------------------------------
    BBFrame is the standard data format used in the BrokerBot project.

        It consists of a Pandas dataframe in the following configuration:
            ================================================================
            |      |  Time  |  Open  |  High  |  Low  |  Close  |  Volume  | <- Labelled columns
            |  01  | string |  float |  float | float |  float  |   float  | 
            |  02  | string |  float |  float | float |  float  |   float  | 
            ================================================================
               ^^
               auto-numbered rows (see pandas Dataframe for more info.)

    .............................................................................................................
    """
    @abstractmethod
    def get_account(self):
        '''
        *** Missing Overview ***

            Returns:
                account object for the API
        '''
        pass
    #--------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def get_socket(self):
        '''
        *** Missing Overview ***

            Returns: 
                the socket object for the API
        '''
        pass

# ==================== Producers ===================

    @abstractmethod
    def get_bars(self, ticker, bar_timeframe, num_of_bars):
        '''
        *** Missing Overview ***

            Parameters:
                ticker (str): ticker of a stock 
                start_time (time object): N/A
                bar_timeframe (time object OR str): time of bar data 
                num_of_bars (int): length of bar 
            
            Returns:
                Pandas DataFrame containing the bars data in BrokerBot Standard Format (BBFrame). 
        '''
        pass

# ==================== Mutators ====================

    @abstractmethod
    def set_account(self, account):
        '''
        *** Missing Overview ***

            Parameters:
                account (...): new account to set this one to
        '''
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
#==================================================================================================================

class AlpacaDataHandler(DataHandler):
    """
    Class: AlpacaDataHandler extends DataHandler 

    .............................................................................................................

    Overview
    --------
    A class that takes in data from the Alpaca API, and sends it through to the Strategy Handler in a format that it can natively understand.
    In short, it is responsible for data transfer and formatting from the Alpaca API. 

    .............................................................................................................
    
    Attributes
    ----------
    api_key : int
        ***
    secret_key : int
        ***
    base_url : str
        ***
    socket : str
        ***

    .............................................................................................................

    Methods
    -------
    set_sh_queue(q):
        *** Missing Overview ***
    
    get_account:
        *** Missing Overview ***

    set_account(account):
        *** Missing Overview ***

    get_socket:
        *** Missing Overview ***
    
    get_bars(ticker: str, _start_time: str, _end_time: str, bar_timeframe: str, bar_limit: str):
        *** Missing Overview ***
    
    on_open(ws):
        *** Missing Overview ***
    
    on_message(ws, message):
        *** Missing Overview ***
    
    on_close(ws):
        *** Missing Overview ***
    
    on_error(ws, error):
        *** Missing Overview ***
    
    start_streaming(tickers):
        *** Missing Overview ***
    
    listen(_tickers, channel_name):
        *** Missing Overview ***

    unlisten(ticker, channel_name):
        *** Missing Overview ***
    
    .............................................................................................................

    Standard Data Fromat (BBFrame)
    ------------------------------
    BBFrame is the standard data format used in the BrokerBot project.

        It consists of a Pandas dataframe in the following configuration:
            ================================================================
            |      |  Time  |  Open  |  High  |  Low  |  Close  |  Volume  | <- Labelled columns
            |  01  | string |  float |  float | float |  float  |   float  | 
            |  02  | string |  float |  float | float |  float  |   float  | 
            ================================================================
               ^^
               auto-numbered rows (see pandas Dataframe for more info.)

    .............................................................................................................

    Pending Tasks
    -------------
    1. More concretely define abstract methods for base class
    2. Support more API subclasses

    .............................................................................................................
    """
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
    #--------------------------------------------------------------------------------------------------------------

    def set_sh_queue(self, q):
        self.sh_queue = q

    def get_account(self):
        return self.api_account

    def set_account(self, account):
        self.acount = account

    def get_socket(self):
        return self.ws

    def get_bars(self, ticker: str, _start_time: str, _end_time: str, bar_timeframe: str, bar_limit: str):
        '''
        *** Missing Overview ***

            Parameters: 
                ticker (str): ticker of a stock

                _start_time (str): the initial time we are looking for data of a stock
                    NOTE: time format is in RFC-3339 format (e.g., 2021-03-11T00:00:00-05:00)

                _end_time (str): the ending time of we are looking for data of a stock
                    NOTE: time format is in RFC-3339 format (e.g., 2021-03-11T00:00:00-05:00) 

                bar_timeframe: time frame of the data 
                    NOTE: currently only 1Day, 1Hour, and 1Min timeframes are available 

                bar_limit (str): the number of bars returned within the timeframe 
            
            Returns:
                Pandas DataFrame: contains the bars data 
        '''
        start_time = datetime.datetime.fromtimestamp(_start_time.time()).strftime('%Y-%m-%dT%H:%M:%S')
        end_time = datetime.datetime.fromtimestamp(_end_time).strftime('%Y-%m-%dT%H:%M:%S')
        url ='https://data.alpaca.markets/v2/stocks'+'/'+ticker+'/bars?adjustment=raw'+'&start='+start_time+'&end='+end_time+'&limit='+bar_limit+'&page_token='+'&timeframe='+bar_timeframe
        r = requests.get(url, headers=self.headers)
        df = pd.read_json(json.dumps(r.json()['bars']))
        df['oi'] = -1
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Open Interest']
        print(df)
        return df
    #--------------------------------------------------------------------------------------------------------------

    #============================================== SOCKET FUNCTIONS ================================================

    def on_open(self, ws):
        '''
        The function is called whenever a websocket is opened, and it authenticates with alpaca 

            Parameters:
                ws (str): websocket
        '''
        print("on open")

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
                "streams": [f"AM.{self.pending_tickers.pop()}"]
            }
        }
        # check pending tickers, sne initial listen message, wait for new tickers,
        ws.send(json.dumps(listen_message))
    #--------------------------------------------------------------------------------------------------------------

    def on_message(self, ws, message):
        '''
        *** Missing Overview ***

            Parameters:
                ws (str): reference to WebSocketApp 
                message (str): message that was received 
        '''
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
    #--------------------------------------------------------------------------------------------------------------

    def on_close(self, ws):
        '''
        *** Missing Overview ***

            Parameters: 
                ws (str): *** Missing Description ***
        '''
        print("closed connection")
    #--------------------------------------------------------------------------------------------------------------

    def on_error(self, ws, error):
        '''
        *** Missing Overview ***

            Parameters: 
                ws (str): *** Missing Description ***
                error (str): *** Missing Description ***
        '''
        print(error)
    #--------------------------------------------------------------------------------------------------------------

    def start_streaming(self, tickers):
        '''
        *** Missing Overview ***

            Parameters: 
                tickers (str): *** Missing Description ***
        '''
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
    #--------------------------------------------------------------------------------------------------------------

    def listen(self, _tickers, channel_name):
        '''
        The function that sends a listen message to alpaca for the streams inputted.

            Parameters:
                _tickers (str): *** Missing Description ***
                channel_name (str): *** Missing Description *** 
        '''
        tickers = []
        for x in range(len(_tickers)):
            tickers.append(channel_name + "." + _tickers[x])
        print(tickers)
        listen_message = {"action": "listen", "data": {"streams": tickers}}
        self.ws.send(json.dumps(listen_message))
        #self.stream_conn.run(quote_callback, tickers)
    #--------------------------------------------------------------------------------------------------------------

    def unlisten(self, ticker, channel_name):
        '''
        The function that unlistens for the streams inputted. 
        NOTE: Might need error checking if a stream that is not currently being listened to is asked to be unlistened. 

            Parameters:
                ticker (str): *** Missing Description ***
                channel_name (str): *** Missing Description *** 
        '''
        for x in range(ticker):
            ticker[x] = channel_name + ticker[x]
        unlisten_message = {"action": "unlisten", "data": {"streams": ticker}}
        self.ws.send(json.dumps(unlisten_message))
    #--------------------------------------------------------------------------------------------------------------
#==================================================================================================================