# bot.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from trade_manager import TradeManager
from analytics import Analytics
from sandbox import Sandbox
from utils import EmergencyHandler

TOKEN = "8146985739"  # Keep quotes, no extra spaces

# Initialize core modules
trade_manager = TradeManager()
analytics = Analytics()
sandbox = Sandbox()
emergency = EmergencyHandler(trade_manager)

# ------------------------
# Telegram Command Handlers
# ------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to PolyPulse Bot!\nUse /trade to execute, /status for dashboard, /kill for emergency stop."
    )

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = await trade_manager.execute_trade()
    await update.message.reply_text(result)

async def
