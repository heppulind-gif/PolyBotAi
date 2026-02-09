# bot.py (Optimized for responsiveness)
import asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from trade_manager import TradeManager
from analytics import Analytics
from sandbox import Sandbox
from utils import EmergencyHandler

# ------------------------
# Configuration
# ------------------------
TOKEN = "8146985739" # keep quotes, no extra spaces

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

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dashboard = analytics.get_dashboard()
    await update.message.reply_text(dashboard)

async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    emergency.activate_kill_switch()
    await update.message.reply_text("Emergency Kill Switch activated. All trading paused.")

# Test command to verify bot responsiveness
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong! ✅ Bot is responsive.")

# ------------------------
# Setup Telegram Application
# ------------------------
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("trade", trade))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("kill", kill))
app.add_handler(CommandHandler("ping", ping))

# ------------------------
# Main Async Loop
# ------------------------
async def main():
    # Run sandbox and trade manager in background tasks
    asyncio.create_task(sandbox.run_simulations())
    asyncio.create_task(trade_manager.monitor_markets())

    # Start Telegram bot
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
