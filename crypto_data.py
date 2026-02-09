# crypto_data.py
import asyncio
import random
import time
from collections import deque

class CryptoData:
    def __init__(self):
        # Historical data caches
        self.polymarket_history = deque(maxlen=500)
        self.btc_history = deque(maxlen=500)
        self.eth_history = deque(maxlen=500)
        self.link_history = deque(maxlen=500)

        # Simulated WebSocket connection flags
        self.ws_connected = False

    async def connect_ws(self):
        # Simulated low-latency WebSocket connection
        await asyncio.sleep(0.1)
        self.ws_connected = True

    async def get_polymarket
