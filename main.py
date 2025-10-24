from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from handlers.start_handler import start
from handlers.menu_handler import mostra_menu
from handlers.callbacks import gestisci_callback
from handlers.ordine_handler import gestisci_messaggi
import store

# 🔑 Inserisci qui il tuo TOKEN Telegram (sostituisci la stringa)
TOKEN = "7352441179:AAEBLeaXHp4sI8E8tW3twpENwUU-Gp2y3IY"

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # comandi
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", mostra_menu))

    # callback e messaggi
    app.add_handler(CallbackQueryHandler(gestisci_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gestisci_messaggi))

    print("🍕 Bot pizzeria avviato... premi Ctrl+C per uscire.")
    app.run_polling()

if __name__ == "__main__":
    main()
