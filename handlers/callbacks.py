from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data.menu_data import MENU
from notify import invia_notifica_ordine

ordini = {}
stati = {}


# ⚙️ GESTIONE CALLBACK
async def gestisci_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    if user_id not in ordini:
        ordini[user_id] = {}

    await query.answer()

    # ➕ Aggiungi pizza
    if data.startswith("add:"):
        pizza = data.split(":")[1]
        ordini[user_id][pizza] = ordini[user_id].get(pizza, 0) + 1

        totale_pizze = sum(ordini[user_id].values())
        keyboard = crea_menu_keyboard_con_carrello(totale_pizze)

        await query.edit_message_text(
            f"✅ *{pizza}* aggiunta al carrello!\n\n🍕 *Scegli altre pizze o vedi il tuo ordine:*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # 🛒 Mostra ordine
    elif data == "vedi_ordine":
        ordine = ordini.get(user_id, {})
        if not ordine:
            await query.edit_message_text(
                "⚠️ Il carrello è vuoto.\n\nUsa /menu per iniziare a ordinare.",
                parse_mode="Markdown"
            )
            return

        testo = "🧾 *RIEPILOGO ORDINE*\n\n"
        totale = 0
        for pizza, qta in ordine.items():
            prezzo = MENU[pizza] * qta
            totale += prezzo
            testo += f"🍕 {pizza} x{qta} = {prezzo}€\n"

        testo += f"\n💰 *Totale: {totale}€*"

        keyboard = [
            [InlineKeyboardButton("✅ Procedi all’ordine", callback_data="scegli_tipo")],
            [InlineKeyboardButton("➕ Aggiungi pizze", callback_data="torna_menu")],
            [InlineKeyboardButton("❌ Svuota carrello", callback_data="svuota")]
        ]

        await query.edit_message_text(
            testo,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # 🔙 Torna al menu
    elif data == "torna_menu":
        totale_pizze = sum(ordini[user_id].values())
        keyboard = crea_menu_keyboard_con_carrello(totale_pizze)
        await query.edit_message_text(
            "🍕 *MENU PIZZERIA*\n\nScegli una pizza da aggiungere:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ❌ Svuota carrello
    elif data == "svuota":
        ordini[user_id] = {}
        keyboard = crea_menu_keyboard_con_carrello(0)
        await query.edit_message_text(
            "🗑️ *Carrello svuotato.*\n\nScegli una pizza per ricominciare:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # 🚗 Scelta tipo ordine
    elif data == "scegli_tipo":
        keyboard = [
            [InlineKeyboardButton("🚗 Consegna a domicilio", callback_data="consegna")],
            [InlineKeyboardButton("🏠 Ritiro in negozio", callback_data="ritiro")],
        ]
        await query.edit_message_text(
            "📦 *Tipo di ordine:*\nScegli come vuoi riceverlo 👇",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # 📍 Consegna: chiede zona prima del nome
    elif data == "consegna":
        keyboard = [
            [InlineKeyboardButton("🏙️ Dentro Valenza (+2€)", callback_data="zona_dentro")],
            [InlineKeyboardButton("🌆 Fuori Valenza (+4€)", callback_data="zona_fuori")],
            [InlineKeyboardButton("⬅️ Indietro", callback_data="scegli_tipo")]
        ]
        await query.edit_message_text(
            "📍 *Zona di consegna:*\nScegli dove vuoi ricevere l’ordine:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ➕ Zona dentro Valenza
    elif data == "zona_dentro":
        context.user_data["consegna_extra"] = 2
        stati[user_id] = "nome"
        context.user_data["modalita"] = "consegna"
        await query.edit_message_text(
            "👤 Inserisci il tuo *nome completo:*",
            parse_mode="Markdown"
        )

    # ➕ Zona fuori Valenza
    elif data == "zona_fuori":
        context.user_data["consegna_extra"] = 4
        stati[user_id] = "nome"
        context.user_data["modalita"] = "consegna"
        await query.edit_message_text(
            "👤 Inserisci il tuo *nome completo:*",
            parse_mode="Markdown"
        )

    # 🏠 Ritiro in negozio
    elif data == "ritiro":
        context.user_data["consegna_extra"] = 0
        stati[user_id] = "nome"
        context.user_data["modalita"] = "ritiro"
        context.user_data["indirizzo"] = "Ritiro in negozio"
        await query.edit_message_text("👤 Inserisci il tuo *nome completo:*", parse_mode="Markdown")

    # ✅ Conferma finale
    elif data == "conferma_finale":
        ordine = ordini.get(user_id, {})
        totale = sum(MENU[p] * q for p, q in ordine.items())

        # Aggiungi costo consegna se presente
        extra = context.user_data.get("consegna_extra", 0)
        totale += extra

        nome = context.user_data.get("nome", "Cliente")
        indirizzo = context.user_data.get("indirizzo", "Ritiro in negozio")
        telefono = context.user_data.get("telefono", "N/D")
        orario = context.user_data.get("orario", "N/D")

        dettaglio = ""
        for pizza, qta in ordine.items():
            dettaglio += f"🍕 {pizza} x{qta}\n"

        riepilogo = (
            f"✅ *Nuovo ordine confermato!*\n\n"
            f"{dettaglio}"
            f"━━━━━━━━━━━━━━━━\n"
            f"👤 Nome: {nome}\n"
            f"📞 Telefono: {telefono}\n"
            f"📍 Indirizzo: {indirizzo}\n"
            f"⏰ Orario: {orario}\n"
            f"🚗 Consegna extra: +{extra}€\n\n"
            f"💰 Totale: *{totale}€*"
        )

        await query.edit_message_text(
            "✅ Ordine confermato! Grazie per aver ordinato 🍕",
            parse_mode="Markdown"
        )
        await invia_notifica_ordine(riepilogo)

        ordini[user_id] = {}
        stati[user_id] = None


# 🔁 Tastiera menu aggiornata
def crea_menu_keyboard_con_carrello(totale_pizze: int):
    keyboard = [
        [InlineKeyboardButton(f"{p} - {MENU[p]}€", callback_data=f"add:{p}")]
        for p in MENU
    ]
    keyboard.append([InlineKeyboardButton("━━━━━━━━━━━━━━━━", callback_data="ignore")])
    keyboard.append([
        InlineKeyboardButton(f"🛒 Vedi Ordine ({totale_pizze})", callback_data="vedi_ordine")
    ])
    return keyboard

