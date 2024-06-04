import threading
import time
from stream_example.stream_socket import SocketConnection

shared_prices = {}
shared_prices_events = {}
shared_prices_lock = threading.Lock()

# create and start the WebSocket thread
socket_t = SocketConnection(shared_prices, shared_prices_lock, shared_prices_events)
socket_t.daemon = True
socket_t.start()

try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    print("KeyboardInterrupt")