#Imports
# from StrategyHandler import StrategyHandler
# from DataHandler import AlpacaDataHandler
# from threading import Thread
# from queue import PriorityQueue
from ENUMS import *
import alpaca_trade_api as tradeapi
import time
import matplotlib.pyplot as plt
import sys
import itertools
import requests
import json
import pandas as pd
#==================================================================================================================

class PortfolioManager:
    """
    Class: PortfolioManager 
    .............................................................................................................

    Overview
    --------
    Portfolio Manager acts as a basic UI for BrokerBot.
    It allows a user to input commands and outputs basic information about BrokerBot operations 

    .............................................................................................................
    
    Attributes
    ----------
    api_key : int
        api key

    secret_key : int
        secret key

    base_url : str
        base url***

    socket : str
        socket url 
    
    .............................................................................................................

    Methods
    -------
    calc_combos:
        Function to calculate all combinations of strategies
    
    get_input:
        Function to return self.input values

    strat_combs:
        Function to return self.input values
    
    get_total_return:
        Function that returns the user's total all time return
    
    get_todays_return:
        Function that returns the user's return for the current day
    
    get_strat:
        Function that returns current running strategy/strategies
    
    get_current_strat:
        Prints current strategy
    
    get_diversity_score:
        Function that computes a portfolio diversity score based on the current holdings the user has
    
    get_current_liquid_cash:
        Function that returns the user's remaining total of liquid cash left in their account

    get_current_total_stock_value:
        Function that returns the user's current total value they have vested in stocks
    
    get_current_total_crypto_value:
        Function that returns the user's current total value they have vested in crypto
    
    get_balance:
        Function that displays the entire balance of a user
    
    order_history:
        Displays entire order history of a user's account
    
    check_positions:
        Displays all positions of a user's account

    add_strat:
        Adds current strategy to self.strategies
    
    initial_setup:
        Sets the initial values of input
    
    set_alpaca:
        Sets Alpaca API values if alpaca api is selected for Execution Handler (EH)
    
    change_strat:
        Changes the strategy based on user input
    
    change_risk:
        Changes the risk based on user input
    
    add_to_watch_list(strat, ticker):
        Adds a stock ticker or strategy to the user's watch list
    
    remove_from_watch_list(strat, ticker):
        Removes a stock ticker or strategy from the user's watch list
    
    withdraw:
        Function that withdraws money from balance
    
    deposit:
        Function that adds money to balance

    .............................................................................................................

    Pending Tasks
    -------------
    1. Create Constructor
    2. I/O for API's, Strategies, Stop/Loss, Cap
    3. Be able to interface with other classes 

    .............................................................................................................
    """
    # ====================Creators====================
    def __init__(self, api_key, secret_key, base_url, socket):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.socket = socket

        self.headers = {}
        self.api = {}
        self.account_url = ""
        self.order_url = "" 
        self.input = []
        
        self.balance = 0
        self.liquid = 0
        self.assets = 0
        self.active = 0
        self.watch_list = ""
        self.combos = self.calc_combos()
        self.strategies = []

        # inputs in the form [strategy, risk, DH_api, EH_api, stop_loss]
        self.initial_setup()
    #--------------------------------------------------------------------------------------------------------------
        
    # ====================Observers====================

    def calc_combos(self):
        '''
        Function to calculate all combinations of strategies
            
            Returns:
                Combos (list): combinations calculated
        '''
        strats = [1,2,3,4,5,6,7,8,9]
        risks = [1,2,3,4,5,6,7,8,9]
        dh_api = [1,2,3,4,5]
        eh_api = [1,2,3,4]
        stop_loss = [1,2]
        combined = [strats,risks,dh_api,eh_api,stop_loss]
        combos = list(itertools.product(*combined))
        return combos
    #--------------------------------------------------------------------------------------------------------------

    def get_input(self):
        '''
        Function to return self.input values

            Returns:
                self.input
        '''
        return self.input
    #--------------------------------------------------------------------------------------------------------------
    
    def strat_combs(self):
        '''
        Function to return all combinations of strategies

            Returns:
                self.combos
        '''
        #print(self.combos)
        return self.combos
    #--------------------------------------------------------------------------------------------------------------
    
    def get_total_return(self):
        '''
        Function that returns the user's total all time return

            Returns: 
                The total all time return of the user's account 
        '''
        pass
    #--------------------------------------------------------------------------------------------------------------
        
    def get_todays_return(self):
        '''
        Function that returns the user's return for the current day

            Returns:
                the retun of the current day for this user's account
        '''
        pass
    #--------------------------------------------------------------------------------------------------------------

    def get_strat(self):
        '''
        Function that returns current running strategy/strategies

            Returns:
                A list of length 0...n depending on the number of strategies the user is currently using.
                This list contains the current strategies.
        '''
        print(self.strategies)
        return self.strategies
    #--------------------------------------------------------------------------------------------------------------
    
    def get_current_strat(self):
        '''
        Prints current strategy

            Returns: 
                self.input
        '''
        print(self.input)
        return self.input
    #--------------------------------------------------------------------------------------------------------------
    
    def get_diversity_score(self):
        '''
        Function that computes a portfolio diversity score based on the current holdings the user has.

            Returns:
                A number between 0 and 100, 0 meaning the user only has one stock and 100 meaning the user's portfolio is very diverse. 
                The score is computed based on strategies being used the number and diversity of tickers being traded.
        '''
        pass
    #--------------------------------------------------------------------------------------------------------------
        
    def get_current_liquid_cash(self):
        '''
        Function that returns the user's remaining total of liquid cash left in their account.

            Returns:
                A float representing the liquid cash in the user's account.    
        '''
        # TODO: Add functionality for other apis
        print("Liquid Balance: {:.2f}".format(self.liquid))
        return self.liquid
    #--------------------------------------------------------------------------------------------------------------
    
    def get_current_total_stock_value(self):
        '''
        Function that returns the user's current total value they have vested in stocks.

            Returns:
                A float representing the value of all of the user's stocks.
        '''
        pass
    #--------------------------------------------------------------------------------------------------------------
        
    def get_current_total_crypto_value(self):
        '''
        Function that returns the user's current total value they have vested in crypto.

            Returns:
                A float representing the value of all of the user's crypto holdings.
        '''
        pass
    #--------------------------------------------------------------------------------------------------------------
    
    def get_balance(self):
        '''
        Function that displays the entire balance of a user.

            Returns: 
                A number reflecting entire balance of a user.
        '''
        pass
    #--------------------------------------------------------------------------------------------------------------
        
    def order_history(self):
        '''
        Displays entire order history of a user's account.

            Returns:
                Creates chart displaying all orders from a user account
        '''
        orders = self.api.list_orders(status='closed')
        columns = ["Symbol","Type","Date","Shares","Price per Share",
                   "Notional","Amount","Status"]
        table = {i: [] for i in columns}
        for i in orders:
            table['Symbol'].append(i.symbol)
            table['Type'].append(i.side)
            table['Date'].append(str(i.created_at)[:10])
            table['Shares'].append(i.qty)
            table['Price per Share'].append(i.filled_avg_price)
            table['Notional'].append(i.notional)
            if(i.status == 'filled'):
                table['Amount'].append('{:.2f}'.format(float(i.filled_qty)*
                                float(i.filled_avg_price)))
            else:
                table['Amount'].append(0)
            table['Status'].append(i.status)
        df = pd.DataFrame(table)
        print(df)
    #--------------------------------------------------------------------------------------------------------------

    def check_positions(self):
        '''
        Displays all positions of a user's account

            Returns:    
                Creates chart displaying all positions from a user account
        '''
        pos = self.api.list_positions()
        col = ["Symbol","Avg Buy","Profit","Qty","Daily Change","Current Price",
               "Last Day Price","Market Value"]
        table = {i: [] for i in col}
        for i in pos:
            table['Symbol'].append(i.symbol)
            table['Avg Buy'].append("{:.2f}".format(float(i.avg_entry_price)))
            table['Qty'].append(i.qty)
            table['Daily Change'].append("{:.5f}".format(
                                  float(i.change_today)))
            table['Current Price'].append(i.current_price)
            table['Last Day Price'].append(i.lastday_price)
            table['Market Value'].append(i.market_value)
            table['Profit'].append("{:.2f}".format(float(i.qty)*
                            (float(i.current_price)-float(i.avg_entry_price))))
        df = pd.DataFrame(table)
        print(df)
    #--------------------------------------------------------------------------------------------------------------

    def add_strat(self):
        '''
        Adds current strategy to self.strategies

            Returns:
                self.strategies
        '''
        self.strategies.append(self.input.copy())
        return self.strategies
    #--------------------------------------------------------------------------------------------------------------

    def initial_setup(self):
        '''
        Sets the initial values of input
        '''
        # TODO: Add functionality for other api's 

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
        self.add_strat()
        if(self.input[3] == 1):
            self.set_alpaca()
    #--------------------------------------------------------------------------------------------------------------

    def set_alpaca(self):
        '''
        Sets Alpaca API values if alpaca api is selected for Execution Handler
        '''
        self.headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.secret_key
        }
        self.api = tradeapi.REST(self.headers["APCA-API-KEY-ID"],
                                 self.headers["APCA-API-SECRET-KEY"], self.base_url)
        self.account_url = "{}v2/account".format(self.base_url)
        self.order_url = "{}v2/orders".format(self.base_url)
        self.liquid = float(self.api.get_account().cash)
        self.balance = float(self.api.get_account().portfolio_value)
        self.assets = self.balance - self.liquid
    #--------------------------------------------------------------------------------------------------------------

    def change_strat(self):
        '''
        Changes the strategy based on user input.
        '''
        # TODO: Add functionality to stop one strategy and start new one 
        
        print("Enter new Strategy to use: (1-9)")
        strat = int(input())
        name = Strategies(strat).name
        print("Selected Strategy: {}".format(name))
        self.input[0] = strat
        self.add_strat()
    #--------------------------------------------------------------------------------------------------------------

    def change_risk(self):
        '''
        Changes the risk based on user input.
        '''
        # TODO: Add functionality to change risk value used

        print("Enter new Risk to use: (1-9)")
        risk = int(input())
        name = Risk(risk).name
        print("Selected Risk: {}".format(name))
        self.input[1] = risk
        self.add_strat()
    #--------------------------------------------------------------------------------------------------------------

    def add_to_watch_list(self, strat, ticker):
        '''
        Adds a stock ticker or strategy to the user's watch list.
        '''
        pass
    #--------------------------------------------------------------------------------------------------------------
        
    def remove_from_watch_list(self, strat, ticker):
        '''
        Removes a stock ticker or strategy from the user's watch list.
        '''
        pass
    #--------------------------------------------------------------------------------------------------------------

    def withdraw(self):
        '''
        Function that withdraws money from balance.

            Returns: 
                self.liquid (int): a number reflecting new balance 
            
            Throws:
                Assertion if withdraw is greater than balance 
        '''
        # TODO: Add functionality to actually withdraw to various API Accounts

        print("Current Liquid Balance: {:0.2f}".format(self.liquid))
        print("Enter a value to withdraw")
        user = int(input())
        while(user > self.liquid):
            print("Withdraw exceeds balance")
            user = int(input())
        self.liquid -= user
        print("New Liquid Balance: {:0.2f}".format(self.liquid))
        return self.liquid
    #--------------------------------------------------------------------------------------------------------------

    def deposit(self):
        '''
        Function that adds money to balance

            Returns:
                self.liquid (int): a number relfecting entire balance of a user 
        '''
        # TODO: Add functionality to actually deposit to various API Accounts

        print("Current Balance: {:0.2f}".format(self.balance))
        print("Enter a value to deposit")
        user = int(input())
        self.liquid += user
        self.balance += user
        print("New Balance: {:0.2f}".format(self.balance))
        return self.liquid
    #--------------------------------------------------------------------------------------------------------------
#==================================================================================================================