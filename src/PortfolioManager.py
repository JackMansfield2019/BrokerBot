#Imports
# from StrategyHandler import StrategyHandler
# from DataHandler import AlpacaDataHandler
from threading import Thread
from queue import PriorityQueue
from ENUMS import *
import time
import config
import sys

class PortfolioManager:

    # Overview: PortfolioManager acts as a basic UI for BrokerBot.
    #           Allows for a user to input commands and outputs basic
    #           information about BrokerBot operations
    # To Do: Create Constructor. I/O for api's, strategies, stop/loss, cap
    #        Be able to interface with other classes

    # ====================Creators====================
    def __init__(self, api_key, secret_key, base_url, socket):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.socket = socket

        self.headers = {}
        self.account_url = ""
        self.order_url = "" 
        self.input = []

        # inputs in the form [strategy, risk, DH_api, EH_api, stop_loss]
        self.initial_setup()
        
    # ====================Observers====================
    # Overview: Function to return self.input values
    #
    # Requires: none
    # Modifies: none
    # Effects: none
    # Returns: self.input
    # Throws: none
    def get_input(self):
        return self.input

    # ====================Producers====================
    # ====================Mutators====================

    # Overview: Sets the initial values of input
    #
    # Requires: none
    # Modifies: self.input
    # Effects: val of self.input changes based on user input
    # Returns: none
    # Throws: none
    # TODO: Add functionality for other api's

    def initial_setup(self):
        print("Enter the specified Strategy: (1-9)")
        strat = int(input())
        name = Strategies(strat).name
        print("Selected Strategy: {}".format(name))
        print("Enter the specified Risk: (1-9)")
        risk = int(input())
        name = Risk(risk).name
        print("Selected Risk: {}".format(name))
        print("Enter the specified DH_API: (1-5)")
        dh_api = int(input())
        name = DH_API(dh_api).name
        print("Selected DH_API: {}".format(name))
        print("Enter the specified EH_API: (1-4)")
        eh_api = int(input())
        name = EH_API(eh_api).name
        print("Selected EH_API: {}".format(name))
        print("Enter the specified Stop Loss: (1-2)")
        stop_loss = int(input())
        name = Stop_loss(stop_loss).name
        print("Selected Stop Loss: {}".format(name))
        self.input = [strat, risk, dh_api, eh_api, stop_loss]
        if(self.input[3] == '1'):
            self.set_alpaca()

    # Overview: Sets Alpaca API values if alpaca api is selected for EH
    #
    # Requires: none
    # Modifies: self.headers, self.account_url, self.order_url
    # Effects: self.headers takes the api key/secret key and formats to alpaca format
    #          self.account_url takes base url and formats to alpaca format
    #          self.order_url takes base url and formats to alpaca format
    # Returns: none
    # Throws: none
    def set_alpaca(self):
        self.headers = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": secret_key
        }
        self.account_url = "{}/v2/account".format(self.base_url)
        self.order_url = "{}/v2/orders".format(self.base_url)

    # Overview: Changes the strategy based on user input
    #
    # Requires: none
    # Modifies: self.input[0]
    # Effects: self.input[0] changes based on user input
    # Returns: none
    # Throws: none
    # TODO: Add functionality to stop one strategy and start new one
    def change_strat(self):
        print("Enter new Strategy to use: (1-9)")
        strat = int(input())
        name = Strategies(strat).name
        print("Selected Strategy: {}".format(name))
        self.input[0] = strat

    # Overview: Changes the risk based on user input
    #
    # Requires: none
    # Modifies: self.input[1]
    # Effects: self.input[1] changes based on user input
    # Returns: none
    # Throws: none
    # TODO: Add functionality to change risk value used
    def change_risk(self):
        print("Enter new Risk to use: (1-9)")
        risk = int(input())
        name = Risk(risk).name
        print("Selected Risk: {}".format(name))
        self.input[1] = risk
    
    
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
    def get_diversity_score(self):
        pass
    
    
