import config
import requests, json

class execution_handler(object):

    def __init__(self,API_key_id,API_secret_key,base_url):
        self.base_url = base_url
        self.account_url = "{}/v2/account".format(self.base_url)
        self.order_url = "{}/v2/orders".format(self.base_url)
        self.headers = {"APCA-API-KEY-ID": API_key_id, "APCA-API-SECRET-KEY": API_secret_key}
        self.api = tradeapi.REST(headers[APCA-API-KEY-ID],headers[APCA-API-SECRET-KEY],base_url)
        self.api_account = api.get_account()

    def get_account():
        return account

    def create_order(self, symbol, qty, side, type, time_in_force, limit_price=None, stop_price=None,
                    trail_price=None, trail_percent=None, extended_hours=False, client_order_id=None,
                    order_class=None, take_profit=None, stop_loss=None):
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

        r = requests.post(order_url, json=data, headers=self.headers)
        return json.loads(r.content)

    def get_orders(self):
        r = requests.get(self.order_url, headers=self.headers)
        return json.loads(r.content)

    def check_limitations(self,api_account):
        """
        Goes through account details and checks if there are any limitations
        that prevents buying shares. Returns true if no limitations, false otherwise
        """
        return True

    def use_strategy():
        """
        Takes data from stategy handler and buys/sells stocks based on strategy
        """
        return
