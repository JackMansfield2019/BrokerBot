import threading
import websocket
import json


def on_open(ws):
    print("opened")
    auth_data = {
        "action": "authenticate",
        "data": {"key_id": "PKELET6JFR9MH8UC3J8Q", "secret_key": "r3fGG3uCbulKZRLm3ZlRQ7GYngRdwnglmryebr9R"}
    }

    ws.send(json.dumps(auth_data))
    print(14)
    listen_message = {"action": "listen", "data": {"streams": ["T.TSLA"]}}
    print(16)
    ws.send(json.dumps(listen_message))
    print(18)
    self.on_close(ws)

def on_message(ws, message):
    print("received a message")
    print(message)


def on_close(ws):
    print("closed connection")


socket = "ws://127.0.0.1:8765"

# ws = websocket.WebSocketApp(socket, on_open=on_open,
#                             on_message=on_message, on_close=on_close)

ws = websocket.WebSocketApp(socket,
                            on_message=lambda ws, msg: on_message(ws,
                                                                  msg),
                            on_close=lambda ws: on_close(ws),
                            on_open=lambda ws: on_open(ws))


t1 = threading.Thread(target=ws.run_forever, args=())
t1.start()
print(43)
t1.join()