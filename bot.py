# bot.py
import asyncio
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from trade_manager import TradeManager
from analytics import Analytics
from sandbox import Sandbox
from utils import EmergencyHandler

# Bot configuration
TOKEN = "8146985739:AAFU0kQ3U0llvEPepQLk4Cy1tM5H1ZzeL9c"  # replace with your token
bot = Bot(TOKEN) 
trade_manager = TradeManager()
analytics = Analytics()
sandbox = Sandbox()
emergency = EmergencyHandler(trade_manager)

# Telegram Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to PolyPulse Bot! Use /trade to execute, /status for dashboard.")

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Execute a 1-tap trade
    result = await trade_manager.execute_trade()
    await update.message.reply_text(result)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dashboard = analytics.get_dashboard()
    await update.message.reply_text(dashboard)

async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    emergency.activate_kill_switch()
    await update.message.reply_text("Emergency Kill Switch activated. All trading paused.")

# Setup Telegram application
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("trade", trade))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("kill", kill))

# Main async loop
async def main():
    # Start sandbox in background
    asyncio.create_task(sandbox.run_simulations())
    # Start trade manager monitoring loop
    asyncio.create_task(trade_manager.monitor_markets())
    # Start Telegram bot
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
