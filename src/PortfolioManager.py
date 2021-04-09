#Imports
from StrategyHandler import StrategyHandler
from DataHandler import AlpacaDataHandler
from threading import Thread
from queue import PriorityQueue
from enum import Enum
import ENUMS
import time
import config
import sys

"""
class Strategies(Enum):
    SHORT = 1
    MEDIUM = 2
    LONG = 3


class Risk(Enum):
    SHORT_LOW_RISK = 1
    MEDIUM_LOW_RISK = 2
    LONG_LOW_RISK = 3

    SHORT_MEDIUM_RISK = 4
    MEDIUM_MEDIUM_RISK = 5
    LONG_MEDIUM_RISK = 6

    SHORT_HIGH_RISK = 7
    MEDIUM_HIGH_RISK = 8
    LONG_HIGH_RISK = 9


class DH_API(Enum):
    ALPACA = 1

    # BINANCE = 2
    # POLYGON = 3
    # IBKR = 4
    # ALPHA = 5


class EH_API(Enum):
    ALPACA = 1

    # BINANCE = 2
    # IBKR = 3
    # ALPHA = 4


class Stop_loss(Enum):
    RSI = 1
    STATIC = 2
"""

class PortfolioManager:

    # Overview: PortfolioManager acts as a basic UI for BrokerBot.
    #           Allows for a user to input commands and outputs basic
    #           information about BrokerBot operations
    # To Do: Create Constructor. I/O for api's, strategies, stop/loss, cap
    #        Be able to interface with other classes

    # ====================Creators====================
    def __init__(self):
        # All values defaulted to 0
        self.strategy = 0
        self.risk = 0
        self.DH_api = 0
        self.EH_api = 0
        self.stop_loss = 0
    # ====================Observers====================

    # Overview: Main function where basic I/O occurs
    #
    # Modifies: self.api, self.strategy, self.stop_loss, self.risk
    # Effects: Changes values of variables based on user input
    # Returns: Basic Output based on input
    def main(self):
        args = len(sys.argv) - 1
        if(args != 5):
            print("Correct Usage: python-file strategy risk DH_api EH_api" +
                  " stop_loss")
        else:
            self.set_strat(sys.argv[1])
            self.set_risk(sys.argv[2])
            self.set_DH_api(sys.argv[3])
            self.set_EH_api(sys.argv[4])
            self.set_stop_loss(sys.argv[5])

    # ====================Producers====================
    # ====================Mutators====================

    # Overview: Function that sets the strategy based on user input
    #
    # Params: input is the user inputted strategy
    # Requires: strategy is an int 1 to 3
    # Modifies: self.strategy
    # Effects: self.strategy = stratinput
    # Returns: Basic Output based on input
    def set_strat(self, input):
        self.strategy = int(input)
        name = Strategies(self.strategy)
        print("Selected Strategy: {}".format(name))

    # Overview: Function that sets the risk based on user input
    #
    # Params: input is the user inputted risk
    # Requires: risk is an int 1 to 9
    # Modifies: self.risk
    # Effects: self.risk = rinput
    # Returns: Basic Output based on input
    def set_risk(self, input):
        self.risk = int(input)
        name = Risk(self.risk)
        print("Selected Risk: {}".format(name))

    # Overview: Function that sets the DH api
    #
    # Params: input is the user inputted api
    # Requires: api is an int 1 to 5
    # Modifies: self.DH_api
    # Effects: self.DH_api = input
    # Returns: Basic Output based on input
    def set_DH_api(self, input):
        self.DH_api = int(input)
        name = DH_API(self.DH_api)
        print("Selected DH API: {}".format(name))

    # Overview: Function that sets the EH api
    #
    # Params: input is the user inputted api
    # Requires: api is an int 1 to 4
    # Modifies: self.EH_api
    # Effects: self.EH_api = input
    # Returns: Basic Output based on input
    def set_EH_api(self, input):
        self.EH_api = int(input)
        name = EH_API(self.EH_api)
        print("Selected EH API: {}".format(name))

    # Overview: Function that sets the Stop loss
    #
    # Params: input is the user inputted stop loss
    # Requires: api is an int 1 to 2
    # Modifies: self.stop_loss
    # Effects: self.stop_loss = input
    # Returns: Basic Output based on input
    def set_stop_loss(self, input):
        self.stop_loss = int(input)
        name = Stop_loss(self.stop_loss)
        print("Selected Stop Loss: {}".format(name))
    
    
    # Overview: Function that prints the user's
    #           portfolio data
    #
    # Params: self (PortfolioManager Object)
    # Requires: PortfolioManager object has values for current
    #           strategies, inputted risk level, total return,
    #           today's return, etc.
    # Modifies: None
    # Effects: None
    # Returns: None, prints instead
    def print_user_portfolio(self):
        pass
        
    # Overview: Function that returns the user's total all time return
    #
    # Params: self (PortfolioManager Object)
    # Requires: None
    # Modifies: None
    # Effects: None
    # Returns: Returns the total all time return of the user's account
    def get_total_return(self):
        pass
        
    # Overview: Function that returns the user's return for the current day
    #
    # Params: self (PortfolioManager Object)
    # Requires: None
    # Modifies: None
    # Effects: None
    # Returns: Returns the return of the current day for this user's account
    def get_todays_return(self):
        pass
        
    # Overview: Function that returns current running strategy/strategies
    #
    # Params: self (PortfolioManager Object)
    # Requires: None
    # Modifies: None
    # Effects: None
    # Returns: Returns a list of length 0...n depending on the number of
    #          strategies the user is currently using. This list contains
    #          the current strategies.
    def get_strat(self):
        pass
    
    
    # Overview: Function that computes a portfolio diversity score based
    #           on the current holdings the user has.
    #
    # Params: self (PortfolioManager Object)
    # Requires: The user has at least one holding
    # Modifies: None
    # Effects: None
    # Returns: Returns a number between 0 and 100, 0 meaning the user only
    #          has one stock and 100 meaning the user's portfolio is very
    #          diverse. The score is computed based on strategies being
    #          used the number and diversity of tickers being traded.
    def get_diversity_score:
        pass
    
    
