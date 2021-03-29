import requests
import json
import alpaca_trade_api as tradeapi
from abc import ABC, abstractmethod


class ExecutionHandler(ABC):

    @abstractmethod
    def get_account(self):
        pass

    @abstractmethod
    def create_order(self):
        pass

    def create_order_notional(self):
        pass

    @abstractmethod
    def get_orders(self):
        pass

    @abstractmethod
    def check_limitations(self):
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


class AlpacaExecutionHandler(ExecutionHandler):

    # ====================Creators====================

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
    # ====================Observers====================

    # overview: returns the alpaca api account
    #
    # modifies: nothing.
    # effects:  nothing.
    # returns: alpaca api account object
    def get_account(self):
        return self.api_account

    # overview: gets all orders
    #
    # modifies: none
    # effects:  none
    # returns: json containing all orders
    def get_orders(self):
        r = requests.get(self.order_url, headers=self.headers)
        return json.loads(r.content)

    # overview: checks if alpaca account has ability to trade or not
    #
    # modifies: none
    # effects:  none
    # returns: True if account is able to trade. False otherwise
    def check_limitations(self):
        if(self.api_account.trading_blocked or
           self.api_account.account_blocked or self.account_cash <= 0):
            return False
        return True

    # overview: cancels an order based on specified orderid
    #
    # params: orderid = alpaca order id for a particular trade
    # modifies: none
    # effects:  none
    # returns: json containing order details
    def cancel_order(self, orderid):
        delete_url = self.order_url + '/' + orderid
        r = requests.delete(delete_url, headers=self.headers)
        return json.loads(r.content)

    # overview: cancels all existing orders
    #
    # modifies: none
    # effects:  none
    # returns: json containing order details
    def cancel_all_orders(self):
        r = requests.delete(order_url, headers=self.headers)
        return json.loads(r.content)

    # overview: get details of an open position based on specified symbol
    #
    # params: symbol = symbol to check positions
    # modifies: none
    # effects:  none
    # returns: json containing order details
    def get_open_pos(self, symbol):
        open_pos_url = self.position_url + '/' + symbol
        r = requests.get(open_pos_url, headers=self.headers)
        return json.loads(r.content)

    # overview: closes a position based on specified symbol
    #
    # params: symbol = symbol to close
    # modifies: none
    # effects:  none
    # returns: json containing order details
    def close_pos(self, symbol):
        close_pos_url = self.position_url + '/' + symbol
        r = requests.delete(close_pos_url, headers=self.headers)
        return json.loads(r.content)

    # overview: closes all positions
    #
    # params: none
    # modifies: none
    # effects:  none
    # returns: json containing order details
    def close_all_pos(self):
        r = requests.delete(self.position_url, headers=self.headers)
        return json.loads(r.content)

    # overview: creates a quantity bracket order based on specified parameters
    #
    # params: symbol = stock symbol to identify asset to trade
    #         qty = number of shares to trade
    #         side = buy or sell
    #         loss = specified stop loss price
    #         profit = specified profit price
    #         limit = specified limit price. None default
    # modifies: none
    # effects:  none
    # returns: json containing order details
    def bracket_order(self, symbol, qty, side, loss, profit, limit=None):
        take_profit = {
            "limit_price": profit
        }
        stop_loss = {
            "stop_price": loss,
            "limit_price": limit
        }
        r = create_order(symbol, qty, side, "market", "gtc",
                         "bracket", take_profit, stop_loss)
        return r

    # overview: creates a notional brack order based on specified parameters
    #
    # params: symbol = stock symbol to identify asset to trade
    #         notional = dollar amount to trade
    #         side = buy or sell
    #         loss = specified stop loss price
    #         profit = specified profit price
    #         limit = specified limit price. None default
    # modifies: none
    # effects:  none
    # returns: json containing order details
    def bracket_order_notional(self, symbol, notional, side, loss, profit,
                               limit=None):
        take_profit = {
            "limit_price": profit
        }
        stop_loss = {
            "stop_price": loss,
            "limit_price": limit
        }
        r = create_order_notional(symbol, notional, side, "bracket",
                                  take_profit, stop_loss)
        return r

    # overview: dynamically adjusts the stop loss value of an order based on
    #           incoming data. stop value should never decrease
    #
    # params: stop = stop loss number
    #         limit = stop limit number. Default none
    # modifies: none
    # effects:  none
    # returns: json containing order details
    def dynamic_stop_loss(self, stop, limit=None):
        r = replace_order(self.orderID, self.qty, "gtc", limit, stop)
        return r

    # overview: loops until order is filled
    #
    # params: orderID is the order ID which identifies which order to wait
    #         for fill
    # modifies: none
    # effects:  none
    # returns: none
    def fill_order(self, orderID):
        order = self.order_url + '/' + orderid
        r = requests.get(order, headers=self.headers)
        status = json.loads(r.content)['status']
        while(status != "filled"):
            r = requests.get(order, headers=self.headers)
            status = json.loads(r.content)['status']
        return

    # ====================Producers====================

    # ====================Mutators====================

    # overview: Places a quantity order based on parameters and updates
    #           variables accordingly.
    #
    # params: symbol = stock symbol to identify asset to trade
    #         qty = number of shares to trade
    #         side = buy or sell
    #         type = market, limit,stop, stop_limit, trailing_stop
    #         time_in_force = day, gtc, opg, cls, ioc, fok
    #         limit_price = limit price. required if type is limit, stop_limit
    #         stop_price = stop price. required of type is stop, stop_limit
    #         trail_price = trail price. required if type is trailing_stop
    #         trail_percent = trail percent. required if type is trailing_stop
    #         extended_hours = Boolean. If true, order will be eligible to
    #                          execute in premarket/afterhours. Only works with
    #                          type limit and time_in_force day
    #         client_order_id = unique identifier for order. Automatically
    #                           generated if not sent
    #         take_profit = dictionary containing limit_price
    #         stop_loss = dictionary containing stop_price and limit_price
    # modifies: self.orderID, self.symbol, self.qty
    # effects:  self.orderID = alpaca generated order id
    #           self.symbol = symbol
    #           self.qty = qty
    # returns: json containing order details
    def create_order(self, symbol, qty, side, type, time_in_force,
                     order_class=None, take_profit=None, stop_loss=None,
                     limit_price=None, stop_price=None,
                     trail_price=None, trail_percent=None,
                     extended_hours=False, client_order_id=None):
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
        fill_order(self, self.orderID)
        return json.loads(r.content)

    # overview: Places a notional order based on parameters and updates
    #           variables accordingly.
    #
    # params: symbol = stock symbol to identify asset to trade
    #         notional = dollar amount to trade.
    #         side = buy or sell
    #         limit_price = limit price. required if type is limit, stop_limit
    #         stop_price = stop price. required of type is stop or stop_limit
    #         trail_price = trail price. required if type is trailing_stop
    #         trail_percent = trail percent. required if type is trailing_stop
    #         extended_hours = Boolean. If true, order will be eligible to
    #                          execute in premarket/afterhours. Only works with
    #                          type limit and time_in_force day
    #         client_order_id = unique identifier for order. Automatically
    #                           generated if not sent
    #         take_profit = dictionary containing limit_price
    #         stop_loss = dictionary containing stop_price and limit_price
    # modifies: self.orderID, self.symbol, self.qty
    # effects:  self.orderID = alpaca generated order id
    #           self.symbol = symbol
    #           self.qty = qty
    # returns: json containing order details
    def create_order_notional(self, symbol, notional, side, order_class=None,
                              take_profit=None, stop_loss=None,
                              limit_price=None, stop_price=None,
                              trail_price=None, trail_percent=None,
                              extended_hours=False, client_order_id=None):
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
        self.qty = qty
        fill_order(self, self.orderID)
        return json.loads(r.content)

    # overview:
    #
    # modifies:
    # effects:
    # returns:
    def trade_signal(self):
        """
        Takes data from stategy handler and buys/sells stocks based on strategy
        """
        return

    # overview: determines number of shares to buy based on explicitly
    #           specified cap value and risk value
    #
    # params: cap = percent of account balance to risk
    #         risk = stop loss amount. Ex. If share is 100 and stop_loss = 95,
    #                risk is 100-95=5
    # modifies: self.qty
    # effects:  self.qty = number of shares calculated based on capped formula
    # returns: self.qty
    def money_alloc_pre(self, cap, risk):
        shares = (self.account.cash*cap)/risk
        shares = int(shares//1)
        self.qty = shares
        return self.qty

    # overview: determines number of shares to buy based on win rate and
    #           win/loss ratio determined from historical data
    #
    # params: win = win rate.
    #         ratio = win/loss rate
    # modifies: self.qty
    # effects:  self.qty = number of shares calculated based on Kelly Criterion
    # returns: self.qty
    def money_alloc_post(self, win, ratio):
        k = win - ((1-win)/ratio)
        shares = self.account.cash*k
        shares = int(shares//1)
        self.qty = shares
        return self.qty

    # overview: replaces an order based on specified parameters
    #
    # params: orderid = alpaca order id for a particular trade
    #         qty = new updated quantity if changed
    #         time_in_force = day, gtc, opg, cls, ioc, fok
    #         limit_price = limit price. required if type is limit, stop_limit
    #         stop_price = stop price. required of type is stop or stop_limit
    #         trail = new value of trail_price or trail_percent value
    #         client_order_id = unique identifier for order. Automatically
    #                           generated if not sent
    # modifies: self.qty
    # effects:  self.qty = updated quantity if changed
    # returns: json containing new order details
    def replace_order(self, orderid, qty, time_in_force, limit_price=None,
                      stop_price=None, trail=None, client_order_id=None):
        replace_url = self.order_url + '/' + orderid
        data = {
            "qty": qty,
            "time_in_force": time_in_force,
            "limit_price": limit_price,
            "stop_price": stop_price,
            "trail": trail,
            "client_order_id": client_order_id,
        }
        self.qty = qty
        r = requests.patch(replace_url, json=data, headers=self.headers)
        return json.loads(r.content)
