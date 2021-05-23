import requests
import json
import alpaca_trade_api as tradeapi
from abc import ABC, abstractmethod
#==================================================================================================================

class ExecutionHandler(ABC):

    """
    Abstract Class for the ExecutionHandler. Outlines essential function signatures.
    """
    # ====================Creators====================

    @abstractmethod
    def __init__(self):
        pass
    # ====================Observers====================

    @abstractmethod
    def get_account(self):
        pass

    @abstractmethod
    def get_orders(self):
        pass

    @abstractmethod
    def check_limitations(self):
        pass

    def cancel_order(self):
        pass

    def cancel_all_orders(self):
        pass

    def get_open_pos(self):
        pass

    @abstractmethod
    def close_pos(self):
        pass

    @abstractmethod
    def close_all_pos(self):
        pass

    @abstractmethod
    def bracket_order(self):
        pass

    @abstractmethod
    def dynamic_stop_loss(self):
        pass

    @abstractmethod
    def fill_order(self):
        pass

    # ====================Mutators====================

    @abstractmethod
    def create_order(self):
        pass

    def create_order_notional(self):
        pass

    @abstractmethod
    def trade_signal(self):
        pass

    @abstractmethod
    def money_alloc_pre(self):
        pass

    @abstractmethod
    def money_alloc_post(self):
        pass

    @abstractmethod
    def replace_order(self):
        pass
#==================================================================================================================

class AlpacaExecutionHandler(ExecutionHandler):
    """
    Class: AlpacaExecutionHandler extends ExecutionHandler 

    .............................................................................................................

    Overview
    --------
    A class that takes in data from given brokerage API, receives signals from the Strategy Handler, and puts in 
    buy/sell order requests through said API. 
    Strategy Handler determines which stock to buy. 
    Execution Handler decides how many shares to buy based on information passed in from the Strategy Handler.
    The symbol, quantity or notional, and current OrderID are stored as local variables. 

    .............................................................................................................
    
    Attributes
    ----------
    API_key_id : int
        api key 

    API_secret_key : int
        api secret key

    base_url : str 
        url for accessing api ****

    .............................................................................................................

    Methods
    -------
    get_account:
        Returns the Alpaca api account. 
    
    check_limitations:
        Checks if alpaca account has ability to trade or not. 
    
    cancel_order(orderid):
        Cancels an order based on specified order id.
    
    cancel_all_orders:
        Cancels all existing orders.

    get_open_pos(symbol):
        Get details of an open position based on specified symbol.

    close_pos(symbol):
        Closes a position based on specified symbol

    close_all_pos:
        Closes all positions.
    
    bracket_order(symbol, qty, side, loss, limit=None):
        Creates a quantity bracket order based on specified parameters.

    dynamic_stop_loss(stop, limit=None):
        Dynamically adjusts the stop loss value of an order based on incoming data.
        Stop value should never decrease.
    
    fill_order(orderID):
        loops until order is filled
    
    create_order(self, symbol, qty, side, type, time_in_force,
                    order_class=None, take_profit=None, stop_loss=None,
                    limit_price=None, stop_price=None,
                    trail_price=None, trail_percent=None,
                    extended_hours=False, client_order_id=None):
        Places a quantity order based on parameters and updates variables accordingly.
    
    create_order_notional(self, symbol, notional, side, order_class=None,
                            take_profit=None, stop_loss=None,
                            limit_price=None, stop_price=None,
                            trail_price=None, trail_percent=None,
                            extended_hours=False, client_order_id=None):
        Places a notional order based on parameters and updates variables accordingly.

    get_orders:
        Gets all active orders.
    
    trade_signal:
        Takes data from stategy handler and buys/sells stocks based on strategy.

    money_alloc_pre(cap, risk):
        Determines number of shares to buy based on explicitly specified cap value and risk value.

    money_alloc_post(win, ratio):
        Determines number of shares to buy based on win rate and win/loss ratio determined from historical data.
    
    replace_order(self, orderid, qty, time_in_force, limit_price=None,
                    stop_price=None, trail=None, client_order_id=None):
        Replaces an order based on specified parameters.
    
    .............................................................................................................
    """
    def __init__(self, API_key_id, API_secret_key, base_url):
        self.base_url = base_url
        self.account_url = "{}/v2/account".format(self.base_url)
        self.order_url = "{}/v2/orders".format(self.base_url)
        self.headers = {"APCA-API-KEY-ID": API_key_id,
                        "APCA-API-SECRET-KEY": API_secret_key}
        self.api = tradeapi.REST(self.headers["APCA-API-KEY-ID"],
                                 self.headers["APCA-API-SECRET-KEY"], base_url)
        self.api_account = self.api.get_account()
        self.account_cash = self.api_account.cash
        self.position_url = "{}/v2/positions".format(self.base_url)
        self.symbol = None
        self.qty = 0
        self.orderID = None
    #--------------------------------------------------------------------------------------------------------------

    def get_account(self):
        '''
        Returns the alpaca api account.

            Returns:
                api_account (...): alpaca api account object 
        '''
        return self.api_account
    #--------------------------------------------------------------------------------------------------------------

    def check_limitations(self):
        '''
        Checks if alpaca account has ability to trade or not
            
            Returns:
                True (bool): if account is able to trade
                False (bool): otherwise 
        '''
        if(self.api_account.trading_blocked or
           self.api_account.account_blocked or float(self.account_cash) <= 0):
            return False
        return True
    #--------------------------------------------------------------------------------------------------------------

    def cancel_order(self, orderid):
        '''
        Cancels an order based on specified order id 

            Parameters:
                orderid (int): the id of the alpaca order 
            Returns:
                json: contains order details 
        '''
        delete_url = self.order_url + '/' + orderid
        r = requests.delete(delete_url, headers=self.headers)
        return json.loads(r.content)
    #--------------------------------------------------------------------------------------------------------------

    def cancel_all_orders(self):
        '''
        Cancels all existing orders. 

            Returns:
                json: contains order details 
        '''
        r = requests.delete(order_url, headers=self.headers)
        return json.loads(r.content)
    #--------------------------------------------------------------------------------------------------------------

    def get_open_pos(self, symbol):
        '''
        Get details of an open position based on specificed symbol

            Parameters: 
                symbol (str): stock symbol
            Returns: 
                json: contains order details
        '''
        open_pos_url = self.position_url + '/' + symbol
        r = requests.get(open_pos_url, headers=self.headers)
        return json.loads(r.content)
    #--------------------------------------------------------------------------------------------------------------

    def close_pos(self, symbol):
        '''
        Closes a position based on specified symbol

            Parameters:
                symbol (str): stock symbol
            Returns: 
                json: contains order details
        '''
        close_pos_url = self.position_url + '/' + symbol
        r = requests.delete(close_pos_url, headers=self.headers)
        return json.loads(r.content)
    #--------------------------------------------------------------------------------------------------------------

    def close_all_pos(self):
        '''
        Closes all positions

            Returns:
                json: contains order details
        '''
        r = requests.delete(self.position_url, headers=self.headers)
        return json.loads(r.content)
    #--------------------------------------------------------------------------------------------------------------

    def bracket_order(self, symbol, qty, side, loss, limit=None):
        '''
        Creates a quantity bracket order based on specified parameters

            Parameters: 
                symbol (str): stock symbol
                qty (int): number of shares to trade
                side (...): buy or sell
                loss (float): specified stop loss price
                profit (float): specified take profit price 
                limit (float): specified limit price (Default: None) 
            
            Returns:
                json: contains order details
        '''
        stop_loss = {
            "stop_price": loss,
            "limit_price": limit
        }
        r = self.create_order(symbol, qty, side, "market", "gtc",
                              "oto", None, stop_loss)
        return r
    #--------------------------------------------------------------------------------------------------------------

    def dynamic_stop_loss(self, stop, limit=None):
        '''
        Dynamically adjusts the stop loss value of an order based on incoming data.
        Stop value should never decrease. 

            Parameters:
                stop (int): stop loss number
                limit (float): stop limit price (Defualt: None)

            Returns:
                json: contains order details
        '''
        self.get_orders()
        r = self.replace_order(self.orderID, self.qty, "gtc", limit, stop)
        return r
    #--------------------------------------------------------------------------------------------------------------

    def fill_order(self, orderID):
        '''
        Loops until order is filled.

            Parameters:
                orderID (int): order ID which identifies which order to wait for fill 
        '''
        order = self.order_url + '/' + orderID
        r = requests.get(order, headers=self.headers)
        status = json.loads(r.content)['status']
        while(status != "filled"):
            r = requests.get(order, headers=self.headers)
            status = json.loads(r.content)['status']
        return
    #--------------------------------------------------------------------------------------------------------------

    def create_order(self, symbol, qty, side, type, time_in_force,
                     order_class=None, take_profit=None, stop_loss=None,
                     limit_price=None, stop_price=None,
                     trail_price=None, trail_percent=None,
                     extended_hours=False, client_order_id=None):
        '''
        Places a quantity order based on parameters and updates variables accordingly. 

            Parameters:
                symbol (str): stock symbol to identify asset to trade
                qty (int): number of shares to trade
                side (...): buy or sell
                type (...): market, limit,stop, stop_limit, trailing_stop
                time_in_force (...): day, gtc, opg, cls, ioc, fok
                limit_price (float): limit price
                        - NOTE: Required if type is limit, stop_limit
                stop_price (float): stop price
                        - NOTE: Required of type is stop, stop_limit
                trail_price (float): trail price
                        - NOTE: Required if type is trailing_stop
                trail_percent (float): trail percent
                        - NOTE: Required if type is trailing_stop
                extended_hours (bool): 
                    If true, order will be eligible to execute in premarket/afterhours
                    NOTE: Only works with type limit and time_in_force day
                client_order_id (int): unique identifier for order
                    NOTE: Automatically generated if not sent
                take_profit (dict): contains limit_price
                stop_loss (dict): contains stop_price and limit_price
            
            Returns:
                json: contains order details
        '''
        data = {
            "symbol": symbol,
            "qty": qty,
            "side": side,
            "type": type,
            "time_in_force": time_in_force,
            "limit_price": limit_price,
            "stop_price": stop_price,
            "trail_price": trail_price,
            "trail_percent": trail_percent,
            "extended_hours": extended_hours,
            "client_order_id": client_order_id,
            "order_class": order_class,
            "take_profit": take_profit,
            "stop_loss": stop_loss
        }

        r = requests.post(self.order_url, json=data, headers=self.headers)
        self.orderID = json.loads(r.content)['id']
        self.symbol = symbol
        self.qty = qty
        self.fill_order(self.orderID)
        return json.loads(r.content)
    #--------------------------------------------------------------------------------------------------------------

    def create_order_notional(self, symbol, notional, side, order_class=None,
                              take_profit=None, stop_loss=None,
                              limit_price=None, stop_price=None,
                              trail_price=None, trail_percent=None,
                              extended_hours=False, client_order_id=None):
        '''
        Places a notional order based on parameters and updates variables accordingly. 

            Parameters:
                symbol (str): stock symbol
                notional (***float or int***): dollar amount to trade 
                side (...): buy or sell
                limit_price (float): limit price
                    NOTE: Required if type is limit, stop_limit 
                stop_price (float): stop price
                    NOTE: Required if type is stop_limit
                trail_price (float): trail price
                    NOTE: Required if type is trailing_stop
                trail_percent: trail percent
                    NOTE: Required if type is trailing_stop
                extended_hours (bool): 
                    If true, order will be eligible to execute in premarket/afterhours.
                    Only wokrs with type limit and time_in_fore day 
                client_order_id (int): unique identifier for order
                    NOTE: Automatically generated if not sent
                take_profit (dict): contains limit_price
                stop_loss (dict): contains stop_price and limit_price

            Returns:
                json: contains order details 
        '''
        data = {
            "symbol": symbol,
            "notional": notional,
            "side": side,
            "type": 'market',
            "time_in_force": 'day',
            "limit_price": limit_price,
            "stop_price": stop_price,
            "trail_price": trail_price,
            "trail_percent": trail_percent,
            "extended_hours": extended_hours,
            "client_order_id": client_order_id,
            "order_class": order_class,
            "take_profit": take_profit,
            "stop_loss": stop_loss
        }

        r = requests.post(self.order_url, json=data, headers=self.headers)
        self.orderID = json.loads(r.content)['id']
        self.symbol = symbol
        self.fill_order(self.orderID)
        return json.loads(r.content)
    #--------------------------------------------------------------------------------------------------------------

    def get_orders(self):
        '''
        Gets all active orders 

            Returns:
                json: contains all orders    
        '''
        r = requests.get(self.order_url, headers=self.headers)
        length = len(json.loads(r.content))
        self.orderID = json.loads(r.content)[length-1]['id']
        self.qty = json.loads(r.content)[length-1]['qty']
        return json.loads(r.content)
    #--------------------------------------------------------------------------------------------------------------

    def trade_signal(self):
        '''
        Takes data from stategy handler and buys/sells stocks based on strategy
        '''
        return
    #--------------------------------------------------------------------------------------------------------------

    def money_alloc_pre(self, cap, risk):
        '''
        Determines number of shares to buy based on explicitly specified cap value and risk value

            Parameters: 
                cap (float): percent of account balance to risk
                risk (int): stop loss amount 
                    ex. If share is 100 and stop_loss = 95, risk is 100 - 95 = 5 
            
            Returns: 
                self.qty (int): number of shared calculated based on capped formula
        '''
        shares = (self.account.cash*cap)/risk
        shares = int(shares//1)
        self.qty = shares
        return self.qty
    #--------------------------------------------------------------------------------------------------------------

    def money_alloc_post(self, win, ratio):
        '''
        Determines number of shares to buy based on win rate and win/loss ratio determined from historical data
            
            Parameters:
                win (int): win rate
                ratio (int): win/loss rate
            
            Returns:
                self.qty (int): number of shares calculated based on Kelly Criterion 
        '''
        k = win - ((1-win)/ratio)
        shares = self.account.cash*k
        shares = int(shares//1)
        self.qty = shares
        return self.qty
    #--------------------------------------------------------------------------------------------------------------

    def replace_order(self, orderid, qty, time_in_force, limit_price=None,
                      stop_price=None, trail=None, client_order_id=None):
        '''
        Replaces an order based on specified parameters

            Parameters:
                orderid (int): aplaca order id for a particular trade
                qty (int): new updated quantity if changed
                time_in_force (...): day, gtc, opg, cls, ioc, fok
                limit_price (float): limit price
                    NOTE: Required if type is limit, stop_limit 
                stop_price (float): stop price
                    NOTE: Required if type is stop or stop_limit
                trail (float): new value of trail_price or trail_percent value
                client_order_id (int): unique identifier for order
                    NOTE: Automatically generated if not sent

            Returns:
                json: contains new order details
        '''
        replace_url = self.order_url + '/' + orderid
        data = {
            "qty": qty,
            "time_in_force": time_in_force,
            "limit_price": limit_price,
            "stop_price": stop_price,
            "trail": trail,
            "client_order_id": client_order_id,
        }
        r = requests.patch(replace_url, json=data, headers=self.headers)
        return json.loads(r.content)
    #--------------------------------------------------------------------------------------------------------------
#==================================================================================================================