# orderbook_analyzer.py
import random
import asyncio

class OrderBookAnalyzer:
    def __init__(self):
        # Stores simulated order book snapshots
        self.orderbook_history = []
        # Minimum liquidity threshold to execute trades safely
        self.min_liquidity = 0.05  # Example value (5% of market)

    async def fetch_orderbook(self, market="POLY"):
        """
        Simulate fetching order book data
        Returns dict: {"bids": float, "asks": float, "spread": float}
        """
        bids = random.uniform(0.4, 0.6)
        asks = random.uniform(0.4, 0.6)
        spread = abs(bids - asks)
        snapshot = {"bids": bids, "asks": asks, "spread": spread, "time": asyncio.get_event_loop().time()}
        self.orderbook_history.append(snapshot)
        if len(self.orderbook_history) > 500:
            self.orderbook_history.pop(0)
        return snapshot

    def is_liquid(self, snapshot):
        """
        Check if market is liquid enough for safe trading
        """
        # Example: if spread too high, consider illiquid
        if snapshot["spread"] > self.min_liquidity:
            return False
        return True

    def confirm_signal(self, signal, snapshot):
        """
        Confirm trade signal based on liquidity and market order book
        Returns adjusted signal: 'UP', 'DOWN', or 'HOLD'
        """
        if not self.is_liquid(snapshot):
            return "HOLD"  # Skip if market illiquid

        # Additional confirmation: check if bid/ask ratio aligns with signal
        bid_ask_ratio = snapshot["bids"] / max(snapshot["asks"], 0.0001)
        if signal == "UP" and bid_ask_ratio < 1:
            return "HOLD"
        elif signal == "DOWN" and bid_ask_ratio > 1:
            return "HOLD"
        return signal

    async def monitor_orderbooks(self, interval=0.5):
        """
        Continuous monitoring of order books for fast decision loops
        """
        while True:
            snapshot = await self.fetch_orderbook()
            # Could be connected to trade manager for live signal adjustments
            await asyncio.sleep(interval)
