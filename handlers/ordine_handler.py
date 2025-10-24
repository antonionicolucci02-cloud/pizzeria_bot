from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from data.menu_data import MENU
from handlers.callbacks import ordini, stati
from notify import invia_notifica_ordine


# ✍️ Gestione messaggi scritti (nome, telefono, indirizzo, orario)
async def gestisci_messaggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    testo = update.message.text
    stato = stati.get(user_id)

    if not stato:
        return

    # 🧍 Nome
    if stato == "nome":
        context.user_data["nome"] = testo
        stati[user_id] = "telefono"
        await update.message.reply_text("📞 Inserisci il tuo *numero di telefono:*", parse_mode="Markdown")

    # 📞 Telefono
    elif stato == "telefono":
        context.user_data["telefono"] = testo

        # Se la modalità è consegna → chiede indirizzo
        if context.user_data.get("modalita") == "consegna":
            stati[user_id] = "indirizzo"
            await update.message.reply_text("🏠 Inserisci il tuo *indirizzo completo:*", parse_mode="Markdown")
        else:
            # Se ritiro → chiede orario
            stati[user_id] = "orario"
            await update.message.reply_text("⏰ Inserisci l’*orario di ritiro:*", parse_mode="Markdown")

    # 🏠 Indirizzo
    elif stato == "indirizzo":
        context.user_data["indirizzo"] = testo
        stati[user_id] = "orario"
        await update.message.reply_text("⏰ Inserisci l’*orario di consegna:*", parse_mode="Markdown")

    # ⏰ Orario finale
    elif stato == "orario":
        context.user_data["orario"] = testo
        stati[user_id] = "fine"

        ordine = ordini.get(user_id, {})
        nome = context.user_data.get("nome", "Cliente")
        telefono = context.user_data.get("telefono", "N/D")
        indirizzo = context.user_data.get("indirizzo", "Ritiro in negozio")
        orario = context.user_data.get("orario", "N/D")
        totale = sum(MENU[p] * q for p, q in ordine.items())

        dettaglio = ""
        for pizza, qta in ordine.items():
            dettaglio += f"🍕 {pizza} x{qta}\n"

        riepilogo = (
            f"🧾 *RIEPILOGO FINALE*\n\n"
            f"{dettaglio}"
            f"━━━━━━━━━━━━━━━━\n"
            f"👤 Nome: {nome}\n"
            f"📞 Telefono: {telefono}\n"
            f"📍 Indirizzo: {indirizzo}\n"
            f"⏰ Orario: {orario}\n\n"
            f"💰 *Totale: {totale}€*"
        )

        keyboard = [
            [InlineKeyboardButton("✅ CONFERMA ORDINE", callback_data="conferma_finale")],
            [InlineKeyboardButton("❌ Annulla", callback_data="svuota")]
        ]

        await update.message.reply_text(
            riepilogo,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
