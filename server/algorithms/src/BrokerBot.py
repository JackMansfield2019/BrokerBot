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
#==================================================================================================================

class BrokerBot():
    """
    Class: Broker Bot

    .............................................................................................................

    Overview
    --------
    Constructs a BrokerBot instance. 

    .............................................................................................................
    
    Attributes
    ----------
    api_key : int 
        the api key for the api this instance uses 
    secret_key : int
        the secret key for the api this instance constructs 
    base_url : str
        the base url of the api 
    socket : str
        the socket url for communication with the api 

    .............................................................................................................

    Methods
    -------
    update:
        Updates handlers based on portfolio manager values.
    
    get_account:
        Returns the account.
    
    set_market_close:
        Sets market_open to false
    
    set_vars:
        Sets variables based on portfolio manager inputs
    
    get_commands:
        Infinite loop to update portfolio manager values
    
    listen_for_searcher:
        ***Missing Overview***
    
    run:
        Start Strategy Handler on own process via multiprocessing
    
    .............................................................................................................

    Extra Information
    -----------------
    Question: How many tickers are we limited to per API request?
    Answer: 200

    Question: How many tickers are we limited on the sockets?
    Answer: 30 
    .............................................................................................................
    """
    def __init__(self, api_key, secret_key, base_url, socket, search_conn):
        if api_key is None or secret_key is None or base_url is None or socket is None:
            print(api_key)
            print(secret_key)
            print(base_url)
            print(socket)
            raise RuntimeError('BrokerBot initalized with a null')

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
    #--------------------------------------------------------------------------------------------------------------

    def update(self):
        '''
        Updates handlers based on portfolio manager values 
        '''
        # TODO: Add checking for if strategy or risk change and update handlers accordingly 

        if(self.pm.input != self.input):
            self.input = self.pm.input
        pass
    #--------------------------------------------------------------------------------------------------------------

    def get_account(self):
        '''
        Returns the account

            Returns:
                JSON containing the contents of the account 
        '''
        # TODO: figure out what this might throw 

        r = requests.get(self.account_url['alpaca'], headers['alpaca'])
        return json.loads(r.content)
    #--------------------------------------------------------------------------------------------------------------

    def set_market_close(self):
        '''
        Sets market_open to false
        '''
        self.market_open = False
    #--------------------------------------------------------------------------------------------------------------

    def set_vars(self):
        '''
        Sets variables based on portfolio manager inputs
        '''
        self.headers = self.pm.headers
        self.account_url = self.pm.account_url
        self.order_url = self.pm.order_url
    #--------------------------------------------------------------------------------------------------------------

    def get_commands(self):
        '''
        Infinite loop to update portfolio manager values 

            Returns: ***
        '''
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
    #--------------------------------------------------------------------------------------------------------------
        
    def listen_for_searcher(self):
        '''
        ***Missing Overview***
        '''
        while True:
            target_stocks = self.searcher_conn.recv()
            for sh_conn in self.sh_pipe_conns:
                sh_conn.send(target_stocks)
    #--------------------------------------------------------------------------------------------------------------

    def run(self):
        '''
        Start SH on own process via multiprocessing

            Throws:
                RuntimeError on execution
        '''
        # TODO: Figure out strategy logic/pipeline 
        # strategies = ["ST1", "ST2", "ST3"]
        strategies = ["ST1"]

        for strat in strategies:
            bb_sh_conn, sh_bb_conn = Pipe()
            self.sh_pipe_conns.append(bb_sh_conn)
            self.sh_instances.append(StrategyHandler(
                self.api_key, self.secret_key, self.base_url, self.socket, strat, self.input))
        """
        for sh in self.sh_instances:
            self.sh_processes.append(Process(target=sh.run, args=()))

        for proc in self.sh_processes:
            proc.start()
        """
        print("Type q to exit or press 'ENTER':")
        while True:
            if not self.market_open:
                print("Market not open")
                for proc in sh_processes:
                    proc.join()
            else:
                commands = self.get_commands()
                cmd_list = list(commands)
                try:
                    user =  input() #sys.stdin.readline()
                    #time.sleep(1)
                except EOFError:
                    continue

                if(user == 'q'):
                    print("quitting")
                    break
                if(user in cmd_list):
                    commands.get(user)()
                    print("Type q to exit or press 'ENTER':")
                    pass
                else:
                    print(user)
                    print(f"Invalid Input - command options are {cmd_list}")
                    print("Type q to exit or press 'ENTER':")

                self.update()
            
    #--------------------------------------------------------------------------------------------------------------
#==================================================================================================================