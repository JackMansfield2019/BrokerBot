import threading
import websocket
import json
import time


def on_open(ws):
    print("opened")
    auth_data = {
        "action": "authenticate",
        "data": {"key_id": "INSERT_KEY", "secret_key": "INSERT_KEY"}
    }

    ws.send(json.dumps(auth_data))

    listen_message = {"action": "listen", "data": {"streams": ["T.TSLA"]}}

    ws.send(json.dumps(listen_message))


def on_message(ws, message):
    print("WS 1: received a message")
    print(message)
    print()


def on_message2(ws, message):
    print("WS 2: received a message")
    print(message)
    print()


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

ws2 = websocket.WebSocketApp(socket,
                             on_message=lambda ws, msg: on_message2(ws,
                                                                    msg),
                             on_close=lambda ws: on_close(ws),
                             on_open=lambda ws: on_open(ws))


t1 = threading.Thread(target=ws.run_forever, args=())
t2 = threading.Thread(target=ws2.run_forever, args=())

t1.start()
t2.start()

time.sleep(10)
t1.kill()
t2.kill()

print("joined")
