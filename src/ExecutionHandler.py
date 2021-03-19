import config
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
    def money_alloc(self):
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


class AlpacaExecutionHandler(ExecutionHandler):

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

    def get_account(self):
        return self.api_account

    def create_order(self, symbol, qty, side, type, time_in_force,
                     order_class=None, take_profit=None, stop_loss=None,
                     trail_price=None, trail_percent=None,
                     extended_hours=False, client_order_id=None):
        data = {
            "symbol": symbol,
            "qty": qty,
            "side": side,
            "type": type,
            "time_in_force": time_in_force,
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
        return json.loads(r.content)

    def create_order_notional(self, symbol, notional, side, order_class=None,
                              take_profit=None, stop_loss=None,
                              trail_price=None, trail_percent=None,
                              extended_hours=False, client_order_id=None):
        data = {
            "symbol": symbol,
            "notional": notional,
            "side": side,
            "type": 'market',
            "time_in_force": 'day',
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
        return json.loads(r.content)

    def get_orders(self):
        r = requests.get(self.order_url, headers=self.headers)
        return json.loads(r.content)

    def check_limitations(self):
        if(self.api_account.trading_blocked or
           self.api_account.account_blocked or self.account_cash <= 0):
            return False
        return True

    def trade_signal(self):
        """
        Takes data from stategy handler and buys/sells stocks based on strategy
        """
        return

    def money_alloc(self):
        """
        Decides how much money is used to purchase shares
        """
        return

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
        r = requests.patch(replace_url, json=data, headers=self.headers)
        return json.loads(r.content)

    def cancel_order(self, orderid):
        delete_url = self.order_url + '/' + orderid
        r = requests.delete(delete_url, headers=self.headers)
        return json.loads(r.content)

    def cancel_all_orders(self):
        r = requests.delete(order_url, headers=self.headers)
        return json.loads(r.content)

    def get_open_pos(self, symbol):
        open_pos_url = self.position_url + '/' + symbol
        r = requests.get(open_pos_url, headers=self.headers)
        return json.loads(r.content)

    def close_pos(self, symbol):
        close_pos_url = self.position_url + '/' + symbol
        r = requests.delete(close_pos_url, headers=self.headers)
        return json.loads(r.content)

    def close_all_pos(self):
        r = requests.delete(self.position_url, headers=self.headers)
        return json.loads(r.content)

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

    def dynamic_stop_loss(self, stop, limit=None):
        r = replace_order(self.orderID, self.qty, "gtc", limit, stop)
        return r
