from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🍕 *Benvenuto alla Pizzeria di Antonio!*\n\n"
        "Usa /menu per visualizzare il menu e iniziare l'ordine."
    )
    await update.message.reply_text(text, parse_mode="Markdown")
