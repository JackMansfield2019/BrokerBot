import config
import websocket, json

class data_handler(object):
    def __init__(self,API_key_id,API_secret_key,base_url,socket = "wss://data.alpaca.markets/stream"):
        self.headers = {"APCA-API-KEY-ID":API_key_id, "APCA-API-SECRET-KEY":API_secret_key}
        self.base_url = base_url
        self.account_url= "{}/v2/account".format(self.base_url)
        self.order_url = "{}/v2/orders".format(self.base_url)
        self.api = tradeapi.REST(headers[APCA-API-KEY-ID],headers[APCA-API-SECRET-KEY],base_url)
        self.api_account = api.get_account()
        self.ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
        
    def get_account(self):
        return account
    def set_account(self,acc):
        self.acount = acc
    def set_socket(self,socket = "wss://data.alpaca.markets/stream"):
        self.ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
    def get_socket():
        return self.ws
        
    def submit_order(self,symbol, qty, side, type, time_in_force, limit_price=None, stop_price=None, 
                   client_order_id=None, order_class=None, take_profit=None, stop_loss=None, 
                   trail_price=None, trail_percent=None):
        api.submit_order(symbol, qty, side, type, time_in_force, limit_price, stop_price, 
                        client_order_id, order_class, take_profit, stop_loss, 
                        trail_price, trail_percent)
    def on_open(self):
        """
        function called whenever a websocket is opened, authenticates with alpaca
        """
        print("opened-stream")
        auth_data = {
            "action": "authenticate",
            "data": {"key_id": config.API_KEY, "secret_key": config.SECRET_KEY}
        }
        self.ws.send(json.dumps(auth_data))

    def on_message(self, message):
        print("received a message")
        print(message)

    def on_close(self):
        print("closed connection")

    def on_error(self, error):
        print error

    def listen(self,ticker,channel_name):
        """
        function that sends a listen message to alpaca for the streams inputed.
        """
        for x in range ticker
            ticker[x] = channel_name + ticker[x]

        listen_message = {"action": "listen", "data": {"streams": ticker}}
        self.ws.send(json.dumps(listen_message))

    def unlisten(self,ticker,channel_name):
        """
        
        function that unlistens for the streams inputed.
            might need error checking if a stream that is not currently being listened to is asked to be unlistened.
        """
        for x in range ticker
            ticker[x] = channel_name + ticker[x]
        unlisten_message = {"action": "unlisten", "data": {"streams": ticker}}
        self.ws.send(json.dumps(unlisten_message))