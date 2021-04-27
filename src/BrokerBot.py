# import DataHandler
# import ExecutionHandler
from PortfolioManager import *
# from StrategyHandler import StrategyHandler
# from DataHandler import AlpacaDataHandler
from threading import Thread
from queue import PriorityQueue
from enum import Enum
from ENUMS import *
import time
from multiprocessing import Process, Pipe
import os
from StrategyHandler import StrategyHandler

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

# ====================Creators====================
    '''
    Overview: constructs a BrokerBot instance.

    Requires: api_key: the api key for the api this instance uses.
                secret_key: the sectet key for the api this instance constructs
                base_url: the base url of the api.
                socket: the socket url for communication with the api
    Modifies: headers,market_open,api_key,secret_key,base_url,socket,
              account_url,order_url,strategy_handler_processes.
    Effects: headers is inilized and contains api_key, and secret_key
                market_open = true
                api_key stores the api key
                base_url stores the api's base url
                socket contian the api's socket port.
                account url stores a formatted url for the account(alpaca only)
                order url stores a formatted url for the orders(alpaca only)
                strategy_handler_processes is inilized to an empty list
    Returns: volume of the stock that was passed in
    Throws: RunTimeException if any parameter is null.
    TODO: How many tickers are we limited to per API request? Answer: 200
    sockets limited to 30
    '''

    #def __init__(self, api_key, secret_key, base_url, socket, search_conn):
    def __init__(self, api_key, secret_key, base_url, socket, search_conn):
        if api_key is None or secret_key is None or base_url is None or socket is None:
            raise RuntimeError('BrokerBot initalized with a null') from exc

        self.market_open = True
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.socket = socket

        self.headers = {}
        self.account_url = ""
        self.order_url = ""

        self.pm = PortfolioManager(api_key, secret_key, base_url, socket)
        self.input = self.pm.input
        self.set_vars()

        #self.searcher_conn = search_conn
        self.sh_pipe_conns = []
        self.sh_instances = []
        self.sh_processes = []
# ====================Observers====================

    '''
        Overview: Updates handlers based on portfoliomanager values
        Requires: none
        Modifies: none
        Effects: none
        Returns: none
        Throws: none
        TODO: Add checking for if strategy or risk change and update
              handlers accordingly
    '''
    def update(self):
        if(self.pm.input != self.input):
            self.input = self.pm.input
        pass
    '''
        Overview: returns the account

        Requires: none
        Modifies: none
        Effects: none
        Returns: a joson containing the contents of the account.
        Throws: ???
        TODO: figure out what this Might throw
    '''

    def get_account(self):
        r = requests.get(self.account_url['alpaca'], headers['alpaca'])
        return json.loads(r.content)
# ====================Producers====================
# ====================Mutators====================
    '''
        Overview: sets market_open to false

        Requires: none
        Modifies: market_open
        Effects: market_open set to false
        Returns: none
        Throws: none
        TODO:
    '''

    def set_market_close(self):
        self.market_open = False
    '''
        Overview: sets variables based on portfolio manager inputs

        Requires: none
        Modifies: self.headers, self.account_url, self.order_url
        Effects: All three values updated based on PortfolioManager
                 values of them
        Returns: none
        Throws: none
        TODO:
    '''
    def set_vars(self):
        self.headers = self.pm.headers
        self.account_url = self.pm.account_url
        self.order_url = self.pm.order_url
    '''
        Overview: infinite loop to update portfoliomanager values

        Requires: none
        Modifies: self.input
        Effects: self.input updates based on user input
        Returns: none
        Throws: none
        TODO:
    '''
    def get_commands(self):
        return {
            "changestrat": self.pm.change_strat,
            "changerisk": self.pm.change_risk,
            "getstrat": self.pm.get_strat,
            "totalreturn": self.pm.get_total_return,
            "todaysreturn": self.pm.get_todays_return,
            "deposit": self.pm.deposit,
            "withdraw": self.pm.withdraw,
            "balance": self.pm.get_balance,
            "liquidbalance": self.pm.get_current_liquid_cash,
            "getcurrstrat": self.pm.get_current_strat,
            "orderhistory": self.pm.order_history,
            "checkpositions": self.pm.check_positions
        }
        

    def listen_for_searcher(self):
        while True:
            target_stocks = self.searcher_conn.recv()
            for sh_conn in self.sh_pipe_conns:
                sh_conn.send(target_stocks)


    '''
        Overview:  Start SH on own process via multiprocessing

        Requires: none
        Modifies: none
        Effects: none
        Returns: none
        Throws: RuntimeError on execution

        TODO: Specfification & figure out strategy logic/pipeline
    '''

    def run(self):
        # strategies = ["ST1", "ST2", "ST3"]
        strategies = ["ST1"]

        for strat in strategies:
            bb_sh_conn, sh_bb_conn = Pipe()
            self.sh_pipe_conns.append(bb_sh_conn)
            self.sh_instances.append(StrategyHandler(
                self.api_key, self.secret_key, self.base_url, self.socket, strat, self.input))

        for sh in self.sh_instances:
            self.sh_processes.append(Process(target=sh.run, args=()))

        for proc in self.sh_processes:
            proc.start()

        while True:
            if not self.market_open:
                for proc in sh_processes:
                    proc.join()
            else:
                commands = self.get_commands()
                cmd_list = list(commands)
        
                user = input()
                if(user == 'q'):
                    break
                if(user in cmd_list):
                    commands.get(user)()
                    pass
                else:
                    print(f"Invalid Input - command options are {cmd_list}")
                self.update()
