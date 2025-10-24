from telegram import InlineKeyboardButton

def crea_menu_keyboard(menu):
    keyboard = []

    for nome, prezzo in menu.items():
        keyboard.append([
            InlineKeyboardButton(f"{nome} - {prezzo}€", callback_data=f"add:{nome}")
        ])

    # Separatore visivo
    keyboard.append([InlineKeyboardButton("━━━━━━━━━━━━━━━━", callback_data="ignore")])
    # Pulsante per vedere l'ordine
    keyboard.append([InlineKeyboardButton("🛒 Vedi Ordine", callback_data="vedi_ordine")])

    return keyboard
