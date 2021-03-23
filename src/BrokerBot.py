# import DataHandler
# import ExecutionHandler
# import PortfolioManager
import StrategyHandler
from DataHandler import AlpacaDataHandler
from threading import Thread
from queue import PriorityQueue
from enum import Enum
import ENUMS
import time

"""
overview: (description of the class)

TODO: (to do of the class as a whole more long term things)
"""
class BrokerBot:

    """
    Abstract Function:

    Representation Invariant:

    Simple explanation:(if nesscary)
    """

#====================Creators====================
    '''
        Overview: returns the previous 5-minute-volume for the given stock by the client 

        Requires: stock is not null
        Modifies: none
        Effects: none
        Returns: volume of the stock that was passed in 

        TODO: How many tickers are we limited to per API request? Answer: 200 
        sockets limited to 30 
    '''
    def __init__(self, api_key, secret_key, base_url, data_url):
        self.headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": secret_key
        }

        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.data_url = data_url

        self.account_url = "{}/v2/account".format(self.base_url)
        self.order_url = "{}/v2/orders".format(self.base_url)

        self.data_handler = AlpacaDataHandler(self.api_key, self.secret_key,
                                              self.base_url, self.data_url, "ws://127.0.0.1:8765")
        self.strategy_handlers = []
        self.strategy_handler.append(self.api_key, self.secret_key, self.base_url, self.data_url,self.order_url)
        #self.priority_queue = PriorityQueue()
        
#====================Observers====================
    '''
        Overview: spins up Trades on  

        Requires: none
        Modifies: none
        Effects: none
        Returns: none
        Throws: RuntimeError on execution

        TODO: Specfification
    '''
    def get_account(self):
        r = requests.get(self.account_url, headers)
        return json.loads(r.content)
#====================Producers====================
#====================Mutators====================
    '''
        Overview: Creates & runs a Data handler thread that listens to ticker 

        Requires: Ticker list of strings containg ticker symbols
        Modifies: Data_handler
        Effects: Data_handler is initalized and listens to tickers
        Returns: none
        Throws: none

        TODO: Specfification
    '''
    def test_stream_data(self, ticker):
        listening_thread = Thread(target = self.data_handler.start_streaming, args=(ticker,))
        listening_thread.start()
        time.sleep(10)
        update_channel_thread = Thread(target=self.data_handler.listen, args=(["AMC"], "T",))

        update_channel_thread.start()
        # print()
        # self.data_handler.run_socket()
        # self.data_handler.listen([ticker], "T")

        # self.data_handler.listen([ticker], "T")


    '''
        Overview: spins up Trades on  

        Requires: none
        Modifies: none
        Effects: none
        Returns: none
        Throws: RuntimeError on execution

        TODO: Specfification
    '''
    def Run():
        raise RuntimeError('Failed to open database') from exc


