from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.keyboards import crea_menu_keyboard
from data.menu_data import MENU

async def mostra_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = crea_menu_keyboard(MENU)
    await update.message.reply_text(
        "🍕 *MENU PIZZERIA*\n\nScegli una pizza da aggiungere:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
