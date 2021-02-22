import config
import websocket, json


class Searcher:
  def __init__(self,API_key_id,API_secret_key,base_url,socket = "wss://data.alpaca.markets/stream"):
  	
  	self.headers = {"APCA-API-KEY-ID":API_key_id, "APCA-API-SECRET-KEY":API_secret_key}
    self.base_url = base_url
    self.account_url= "{}/v2/account".format(self.base_url)
    self.order_url = "{}/v2/orders".format(self.base_url)
    self.api = tradeapi.REST(
                          headers[APCA-API-KEY-ID],
                          headers[APCA-API-SECRET-KEY],
                          base_url
          )
    self.api_account = api.get_account()
    self.socket = socket

  def get_account(self):
    return account

  def search():
  def get_data():
  def set_socket(self,socket = "wss://data.alpaca.markets/stream"):
    self.socket = socket

  def submit_order(self,symbol, qty, side, type, time_in_force, limit_price=None, stop_price=None, 
                   client_order_id=None, order_class=None, take_profit=None, stop_loss=None, 
                   trail_price=None, trail_percent=None):
    
    api.submit_order(symbol, qty, side, type, time_in_force, limit_price, stop_price, 
                   client_order_id, order_class, take_profit, stop_loss, 
                   trail_price, trail_percent)

  def on_open():
      print("opened-stream")
      auth_data = {
          "action": "authenticate",
          "data": {"key_id": config.API_KEY, "secret_key": config.SECRET_KEY}
      }

      ws.send(json.dumps(auth_data))

      listen_message = {"action": "listen", "data": {"streams": ["AM.TSLA"]}}

      ws.send(json.dumps(listen_message))


  def on_message(ws, message):
      print("received a message")
      print(message)

  def on_close(ws):
      print("closed connection")

  socket = "wss://data.alpaca.markets/stream"

  ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
  ws.run_forever()
