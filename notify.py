import requests

# Inserisci qui il tuo token e l'ID del canale (es: -1001234567890)
TOKEN = "7352441179:AAEBLeaXHp4sI8E8tW3twpENwUU-Gp2y3IY"
CHANNEL_ID = "-1003271816174"

def invia_notifica_ordine(testo):
    """Invia un messaggio di notifica al canale Telegram."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": f"📦 Nuovo ordine ricevuto:\n\n{testo}"
    }
    response = requests.post(url, data=data)
    return response.json()
