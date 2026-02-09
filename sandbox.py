# sandbox.py
import asyncio
import random
from crypto_data import CryptoData
from ml_engine import MLModel
from portfolio_manager import PortfolioManager
from analytics import Analytics

class Sandbox:
    def __init__(self):
        self.crypto_data = CryptoData()
        self.ml_model = MLModel()
        self.portfolio = PortfolioManager()
        self.analytics = Analytics()
        self.running = True
        self.simulation_speed = 0.2  # seconds per micro-decision

    async def run_simulations(self):
        """
        Continuous background sandbox mode:
        - Executes paper trades
        - Tests new strategies
        - Updates portfolio and analytics
        """
        while self.running:
            # Fetch latest market data
            odds = await self.crypto_data.get_polymarket_odds()
            btc, eth, link = await self.crypto_data.get_crypto_data()

            # Predict trade signal
            signal, confidence = self.ml_model.predict(odds, btc, eth, link)

            # Calculate stake & TP/SL
            stake = self.portfolio.calculate_stake(confidence)
            tp, sl = self.portfolio.calculate_tp_sl(confidence)

            # Simulate trade
            profit_loss = self._simulate_trade(signal, stake, tp, sl)

            # Update portfolio & analytics
            self.portfolio.update_balance(profit_loss)
            self.analytics.log_trade(signal, stake, tp, sl, profit_loss, confidence)
            self.analytics.update_market_data(odds, btc, eth, link)

            # Micro-decision speed
            await asyncio.sleep(self.simulation_speed)

    def _simulate_trade(self, signal, stake, tp, sl):
        """
        Simulate realistic P/L based on signal, stake, TP/SL
        """
        # Simulate outcome using random factors influenced by confidence
        multiplier = 1.0
        if signal == "UP":
            multiplier = random.uniform(0.95, 1.05)
        elif signal == "DOWN":
            multiplier = random.uniform(0.95, 1.02)
        else:  # HOLD or uncertain
            multiplier = 1.0
        return stake * (multiplier - 1)
