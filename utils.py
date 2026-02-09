# utils.py
import time
import asyncio

class Logger:
    def __init__(self, logfile="poly_pulse.log"):
        self.logfile = logfile

    def log_trade(self, signal, stake, tp, sl, profit_loss, confidence):
        log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} | Signal: {signal} | Stake: {stake} | TP: {tp} | SL: {sl} | P/L: {profit_loss:.4f} | Confidence: {confidence:.2f}\n"
        with open(self.logfile, "a") as f:
            f.write(log_entry)
        print(log_entry.strip())

    def log_event(self, message):
        log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} | EVENT: {message}\n"
        with open(self.logfile, "a") as f:
            f.write(log_entry)
        print(log_entry.strip())

class EmergencyHandler:
    def __init__(self, trade_manager=None):
        self.kill_switch = False
        self.api_down = False
        self.trade_manager = trade_manager

    def activate_kill_switch(self):
        self.kill_switch = True
        if self.trade_manager:
            self.trade_manager.paper_mode = True  # force paper mode
        print("Emergency Kill Switch Activated!")

    def deactivate_kill_switch(self):
        self.kill_switch = False
        print("Emergency Kill Switch Deactivated!")

    async def monitor_api(self, check_function, interval=2):
        """
        Periodically checks API status and updates api_down flag
        check_function should return True if API is healthy, False otherwise
        """
        while True:
            healthy = check_function()
            self.api_down = not healthy
            await asyncio.sleep(interval)

# Helper functions
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return 0
