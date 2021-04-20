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
import datetime
import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds
import backtrader.strategies as btstrats


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
        self.api = {}
        self.account_url = {}
        self.order_url = {}
        self.pos_url = {}
        self.input = []

        self.balance = 0
        self.liquid = 0
        self.assets = 0
        self.active = 0
        self.buying_power = 0
        self.watch_list = []
        self.crypto_value = 0
        self.combos = self.calc_combos()
        self.strategies = []

        # inputs in the form [strategy, risk, DH_api, EH_api, stop_loss]
        self.initial_setup()

    # ====================Observers====================
    # Overview: Function to calculate all combinations of strategies
    #
    # Requires: none
    # Modifies: none
    # Effects: none
    # Returns: combinations calculated
    # Throws: none
    def calc_combos(self):
        strats = [1,2,3,4,5,6,7,8,9]
        risks = [1,2,3,4,5,6,7,8,9]
        dh_api = [1,2,3,4,5]
        eh_api = [1,2,3,4]
        stop_loss = [1,2]
        combined = [strats,risks,dh_api,eh_api,stop_loss]
        combos = list(itertools.product(*combined))
        return combos

    # Overview: Function to return self.input values
    #
    # Requires: none
    # Modifies: none
    # Effects: none
    # Returns: self.input
    # Throws: none
    def get_input(self):
        return self.input

    # Overview: Function to return all combinations of strategies
    #
    # Requires: none
    # Modifies: none
    # Effects: none
    # Returns: self.combos
    # Throws: none
    def strat_combs(self):
        #print(self.combos)
        return self.combos


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
        print(self.strategies)
        return self.strategies

    # Overview: Prints current strategy
    #
    # Requires: none
    # Modifies: none
    # Effects: none
    # Returns: self.input
    # Throws: none
    # TODO:
    def get_current_strat(self):
        print(self.input)
        return self.input

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

    # Overview: Function that returns the user's remaining total of
    #           liquid cash left in their account.
    #
    # Params: self (PortfolioManager Object)
    # Requires: None
    # Modifies: None
    # Effects: None
    # Returns: A float representing the liquid cash in the user's account.
    # TODO: Add functionality for other apis
    def get_current_liquid_cash(self):
        print("Liquid Balance: {:.2f}".format(self.liquid))
        return self.liquid

    # Overview: Function that returns the user's current total value they have
    #           vested in stocks.
    #
    # Params: self (PortfolioManager Object)
    # Requires: None
    # Modifies: None
    # Effects: None
    # Returns: A float representing the value of all of the user's stock holdings.
    def get_current_total_stock_value(self):
        print("Total Stock Value: {:.2f}".format(self.buying_power - self.crypto_value))
        return self.buying_power - self.crypto_value

    # Overview: Function that returns the user's current total value they have
    #           vested in crypto.
    #
    # Params: self (PortfolioManager Object)
    # Requires: None
    # Modifies: None
    # Effects: None
    # Returns: A float representing the value of all of the user's crypto holdings.
    def get_current_total_crypto_value(self):
        print("Crypto Value: {:.2f}".format(self.crypto_value))
        return self.crypto_value

    # Overview: Function that displays the entire balance of a user
    #
    # Params: self (PortfolioManager Object)
    # Requires: None
    # Modifies: None
    # Effects: None
    # Returns: Returns a number reflecting entire balance of a user
    # TODO: Add functionality for other API's
    def get_balance(self):
        print("Balance Breakdown")
        print("Alpaca: {:.2f}".format(float(self.api['alpaca'].get_account().
                                      portfolio_value)))
        return self.balance

    # Overview: Displays entire order history of a user's account
    #
    # Params: self (PortfolioManager Object)
    # Requires: None
    # Modifies: None
    # Effects: None
    # Returns: Creates chart displaying all orders from a user account
    def order_history(self):
        #If Alpaca API
        if(self.input[3] == 1):
            data = {"status": "all",}
            r = requests.get(self.order_url['alpaca'], params=data, headers=self.headers['alpaca'])
            orders = json.loads(r.content)
            columns = ["Symbol","Type","Date","Shares","Price per Share",
                        "Notional","Amount","Status"]
            table = {i: [] for i in columns}
            for i in orders:
                table['Symbol'].append(i['symbol'])
                table['Type'].append(i['side'])
                table['Date'].append(str(i['created_at'])[:10])
                table['Shares'].append(i['qty'])
                table['Price per Share'].append(i['filled_avg_price'])
                table['Notional'].append(i['notional'])
                if(i['status'] == 'filled'):
                    table['Amount'].append('{:.2f}'.format(float(i['filled_qty'])*
                                    float(i['filled_avg_price'])))
                else:
                    table['Amount'].append(0)
                table['Status'].append(i['status'])
            df = pd.DataFrame(table)
            print(df)

    # Overview: Displays all positions of a user's account
    #
    # Params: self (PortfolioManager Object)
    # Requires: None
    # Modifies: None
    # Effects: None
    # Returns: Creates chart displaying all positions from a user account
    def check_positions(self):
        #If Alpaca API
        if(self.input[3] == 1):
            r = requests.get(self.pos_url['alpaca'], headers=self.headers['alpaca'])
            pos = json.loads(r.content)
            col = ["Symbol","Avg Buy","Profit","Qty","Daily Change","Current Price",
                "Last Day Price","Market Value"]
            table = {i: [] for i in col}
            for i in pos:
                table['Symbol'].append(i['symbol'])
                table['Avg Buy'].append("{:.2f}".format(float(i['avg_entry_price'])))
                table['Qty'].append(i['qty'])
                table['Daily Change'].append("{:.5f}".format(
                                    float(i['change_today'])))
                table['Current Price'].append(i['current_price'])
                table['Last Day Price'].append(i['lastday_price'])
                table['Market Value'].append("{:.2f}".format(float(i['market_value'])))
                table['Profit'].append("{:.2f}".format(float(i['qty'])*
                                (float(i['current_price'])-float(i['avg_entry_price']))))
            df = pd.DataFrame(table)
            print(df)

    # Overview: Liquidates all open positions
    #
    # Params: self (PortfolioManager Object)
    # Requires: None
    # Modifies: None
    # Effects: None
    # Returns: new liquid value
    # TODO: Add functionality for other API's
    def liquidate(self):
        #If Alpaca API
        if(self.input[3] == 1):
            r = requests.delete(self.pos_url['alpaca'], headers=self.headers['alpaca'])
        self.update()
        print("New Liquid Balance: {:.2f}".format(self.liquid))

    # Overview: Analyzes the performance of the current strategy
    #
    # Params: self (PortfolioManager Object)
    # Requires: None
    # Modifies: None
    # Effects: None
    # Returns: various analysis values computed
    # TODO: Add functionality for other API's
    def analyze(self):
        pass

    # ====================Producers====================
    # ====================Mutators====================
    # Overview: Adds current strategy to self.strategies
    #
    # Requires: none
    # Modifies: self.strategies
    # Effects: self.strategies.append(self.input)
    # Returns: self.strategies
    # Throws: none
    # TODO:
    def add_strat(self):
        self.strategies.append(self.input.copy())
        return self.strategies

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
        self.add_strat()
        if(self.input[3] == 1):
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
        self.headers['alpaca'] = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.secret_key
        }
        self.api['alpaca'] = tradeapi.REST(self.headers['alpaca']["APCA-API-KEY-ID"],
                                 self.headers['alpaca']["APCA-API-SECRET-KEY"], self.base_url)
        self.account_url['alpaca'] = "{}/v2/account".format(self.base_url)
        self.order_url['alpaca'] = "{}/v2/orders".format(self.base_url)
        self.pos_url['alpaca'] = "{}/v2/positions".format(self.base_url)
        self.liquid += float(self.api['alpaca'].get_account().cash)
        self.balance += float(self.api['alpaca'].get_account().portfolio_value)
        self.assets += self.balance - self.liquid
        self.buying_power = float(self.api['alpaca'].get_account().buying_power)
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
        self.add_strat()

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
        self.add_strat()

    # Overview: Adds a stock ticker to the user's watch list.
    #
    # Requires: none
    # Modifies: self.watch_list
    # Effects: adds a ticker to self.watch_list
    # Returns: none
    # Throws: none
    def add_to_watch_list(self):
        print("Enter the ticker to add: ")
        ticker = input()
        self.watch_list.append(ticker)

    # Overview: Removes a stock ticker from the user's watch list.
    #
    # Requires: none
    # Modifies: self.watch_list
    # Effects: removes a ticker from self.watch_list
    # Returns: none
    # Throws: none
    def remove_from_watch_list(self):
        print("Enter the ticker to remove: ")
        ticker = input()
        self.watch_list.remove(ticker)

    # Overview: Function that withdraws money from balance
    #
    # Params: None
    # Requires: None
    # Modifies: this.balance
    # Effects: this.balance -= minus
    # Returns: Returns a number reflecting new balance
    # Throws: Assertion if withdraw is greater than balance
    # TODO: Add functionality to actually withdraw to various API Accounts
    def withdraw(self):
        print("Current Liquid Balance: {:0.2f}".format(self.liquid))
        print("Enter a value to withdraw")
        user = int(input())
        while(user > self.liquid):
            print("Withdraw exceeds balance")
            user = int(input())
        self.liquid -= user
        print("New Liquid Balance: {:0.2f}".format(self.liquid))
        return self.liquid

    # Overview: Function that adds money to balance
    #
    # Params: self (PortfolioManager Object)
    # Requires: None
    # Modifies: this.balance
    # Effects: this.balance += plus
    # Returns: Returns a number reflecting entire balance of a user
    # TODO: Add functionality to actually deposit to various API Accounts
    def deposit(self):
        print("Current Balance: {:0.2f}".format(self.balance))
        print("Enter a value to deposit")
        user = int(input())
        self.liquid += user
        self.balance += user
        print("New Balance: {:0.2f}".format(self.balance))
        return self.liquid

    # Overview: Function that updates liquid and asset value
    #
    # Params: self (PortfolioManager Object)
    # Requires: None
    # Modifies: this.liquid, this.assets
    # Effects: liquid and assets are reassigned new values based on api return
    # Returns: None
    # TODO: Add functionality to actually deposit to various API Accounts
    def update(self):
        self.liquid = self.api['alpaca'].cash
        self.balance = self.api['alpaca'].portfolio_value
        self.assets = self.balance - self.liquid
