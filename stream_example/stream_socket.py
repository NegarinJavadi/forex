import threading
import websocket
import json
import uuid
import datetime as dt
from infrastructure.log_wrapper import LogWrapper
from models.api_price import ApiPrice

from stream_example.signature import get_signature, WEB_ID, WEB_KEY


def get_login(id):
    ts = int(dt.datetime.now().timestamp() * 1000)
    sig = get_signature(str(ts))

    login = {
        "Id": id,
        "Request": "Login",
        "Params": {
            "AuthType": "HMAC",
            "WebApiId": WEB_ID,
            "WebApiKey": WEB_KEY,
            "Timestamp": ts,
            "Signature": sig,
            "DeviceId": "WebBrowser",
            "AppSessionId": "1234"
        }
    }

    return login


def login_was_ok(msg_data):
    print(f"login_was_ok: {msg_data}")
    if "Result" in msg_data and "Info" in msg_data["Result"]:
        if msg_data["Result"]["Info"] == "ok":
            return True
    return False


class SocketConnection(threading.Thread):

    def __init__(self, shared_prices, price_lock: threading.Lock, price_events):
        super().__init__()
        self.id = str(uuid.uuid4())
        self.log = LogWrapper("SocketConnection")
        self.price_lock = price_lock
        self.shared_prices = shared_prices
        self.price_events = price_events
        self.pairs_list = shared_prices.keys()

    def log_message(self, msg, error=False):
        if error:
            self.log.logger.error(msg)
        else:
            self.log.logger.debug(msg)

    def run(self):
        ws_url = "wss://marginalttdemowebapi.fxopen.net:3001"
        ws = websocket.WebSocketApp(ws_url)

        def on_open(ws):
            self.log_message("WebSocket connection established")
            l = get_login(self.id)
            self.log_message(f"Login with: {l}")
            ws.send(json.dumps(l))

        def on_message(ws, message):
            msg_data = json.loads(message)
            print("on_message():", msg_data)

        def on_error(ws, error):
            self.log_message(f"WebSocket error occurred: {error}")
            ws.close()

        def on_close(ws, close_status_code, close_msg):
            self.log_message(f"WebSocket connection closed with code: {close_status_code}, message: {close_msg}")

        ws.on_open = on_open
        ws.on_message = on_message
        ws.on_error = on_error
        ws.on_close = on_close

        ws.run_forever()