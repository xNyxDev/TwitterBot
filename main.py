import os
import time
import threading
import schedule
import requests
import tweepy
import json
from flask import Flask
from deep_translator import GoogleTranslator

# ========== CARGA DE VARIABLES DE ENTORNO ==========
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
API_TOKEN = os.environ.get("API_TOKEN")
API_TOKEN_SECRET = os.environ.get("API_TOKEN_SECRET")

# ========== INICIALIZAR CLIENTE DE TWITTER ==========
client = None
try:
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=API_TOKEN,
        access_token_secret=API_TOKEN_SECRET
    )
    print("✅ Cliente de Twitter inicializado con éxito.")
except Exception as e:
    print(f"❌ Error al inicializar el cliente de Twitter: {e}")

# ========== OBTENER DATO INTERESANTE ==========
def obtener_dato_interesante():
    try:
        print("🔍 Obteniendo dato interesante...")
        res = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        raw = res.text.strip().rstrip(";")
        print(f"📥 Respuesta bruta: {raw}")

        if res.status_code == 200:
            try:
                dato_json = json.loads(raw)
                texto_original = dato_json.get("text")
                if texto_original:
                    traducido = GoogleTranslator(source='en', target='es').translate(texto_original)
                    print(f"✅ Traducción: {traducido}")
                    return traducido
                else:
                    print("⚠️ El campo 'text' no está en la respuesta.")
                    return None
            except json.JSONDecodeError as e:
                print(f"⚠️ Error al decodificar JSON: {e} - Respuesta bruta: {raw}")
                return None
        else:
            print(f"⚠️ Código de error HTTP: {res.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión al obtener el dato: {e}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado al procesar el dato: {e}")
        print(f"Detalles del error inesperado: {e}")
        return None

# ========== GUARDAR HISTORIAL ==========
def guardar_en_historial(texto):
    try:
        with open("tweets.log", "a", encoding="utf-8") as log:
            log.write(texto + "\n")
        print("📝 Dato guardado en el historial.")
    except Exception as e:
        print(f"⚠️ No se pudo guardar en el historial: {e}")

# ========== PUBLICAR TWEET ==========
def publicar_tweet():
    if not client:
        print("⚠️ Cliente de Twitter no disponible.")
        return

    dato = obtener_dato_interesante()
    if dato:
        try:
            response = client.create_tweet(text=f"Dato del Día: {dato}")
            tweet_id = response.data['id']
            print(f"✅ Tweet publicado con ID: {tweet_id}")
            guardar_en_historial(f"Tweet ID: {tweet_id} - {dato}")
        except tweepy.TweepyException as e:
            print(f"❌ Error al publicar el tweet: {e}")
    else:
        print("⚠️ No se obtuvo ningún dato para publicar.")

# ========== INICIAR PROGRAMADOR ==========
def iniciar_scheduler():
    print("🕒 Programador de tareas iniciado. Publicando cada 2 minutos.")
    publicar_tweet()
    schedule.every(2).minutes.do(publicar_tweet)
    while True:
        schedule.run_pending()
        time.sleep(1)

# ========== FLASK ==========
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot activo y funcionando. Revisa los logs para ver los tweets enviados."

# ========== MAIN ==========
if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 10000))

    scheduler_thread = threading.Thread(target=iniciar_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    print(f"🚀 Servidor Flask iniciado en http://localhost:{puerto}")
    app.run(host="0.0.0.0", port=puerto)
