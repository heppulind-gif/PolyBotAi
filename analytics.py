# analytics.py
import time
import numpy as np
from collections import deque

class Analytics:
    def __init__(self):
        # Store recent trades for analytics
        self.recent_trades = deque(maxlen=100)
        self.market_history = deque(maxlen=100)
        self.crypto_history = deque(maxlen=100)

    def log_trade(self, signal, stake, tp, sl, profit_loss, confidence):
        self.recent_trades.append({
            "signal": signal,
            "stake": stake,
            "tp": tp,
            "sl": sl,
            "profit_loss": profit_loss,
            "confidence": confidence,
            "time": time.time()
        })

    def update_market_data(self, polymarket_odds, btc_data, eth_data, link_data):
        self.market_history.append(polymarket_odds)
        self.crypto_history.append([btc_data["price"], eth_data["price"], link_data["price"]])

    def get_dashboard(self):
        """
        Returns a formatted string for Telegram dashboard
        Includes:
        - Last trade info
        - Confidence %
        - Predicted ROI
        - Portfolio performance metrics
        """
        if not self.recent_trades:
            return "No trades yet."

        last_trade = self.recent_trades[-1]
        avg_profit = np.mean([t["profit_loss"] for t in self.recent_trades])
        win_rate = np.mean([1 if t["profit_loss"] > 0 else 0 for t in self.recent_trades]) * 100

        dashboard = (
            f"--- PolyPulse Dashboard ---\n"
            f"Last Trade: {last_trade['signal']} | P/L: {last_trade['profit_loss']:.4f}\n"
            f"Confidence: {last_trade['confidence']:.2f}\n"
            f"Avg Profit: {avg_profit:.4f} | Win Rate: {win_rate:.1f}%\n"
            f"Total Trades: {len(self.recent_trades)}"
        )
        return dashboard

    def get_heatmap(self):
        """
        Generates a simple correlation heatmap for BTC/ETH/Chainlink
        Returns a dict of correlation values
        """
        if len(self.crypto_history) < 10:
            return {"BTC_ETH": 0, "BTC_LINK": 0, "ETH_LINK": 0}

        prices = np.array(self.crypto_history)
        btc_prices, eth_prices, link_prices = prices[:,0], prices[:,1], prices[:,2]

        corr_matrix = np.corrcoef([btc_prices, eth_prices, link_prices])
        heatmap = {
            "BTC_ETH": corr_matrix[0,1],
            "BTC_LINK": corr_matrix[0,2],
            "ETH_LINK": corr_matrix[1,2]
        }
        return heatmap

    def get_correlation_map(self):
        """
        Returns a formatted string for Telegram
        """
        heatmap = self.get_heatmap()
        return (
            f"--- Correlation Map ---\n"
            f"BTC-ETH: {heatmap['BTC_ETH']:.2f}\n"
            f"BTC-LINK: {heatmap['BTC_LINK']:.2f}\n"
            f"ETH-LINK: {heatmap['ETH_LINK']:.2f}"
        )
