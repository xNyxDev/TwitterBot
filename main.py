import os
import time
import threading
import schedule
import requests
import tweepy
from flask import Flask
from deep_translator import GoogleTranslator

# Cargar variables de entorno
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
API_TOKEN = os.environ.get("API_TOKEN")
API_TOKEN_SECRET = os.environ.get("API_TOKEN_SECRET")

# Inicializar cliente de Twitter
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

# Obtener un dato interesante desde la API
def obtener_dato_interesante():
    try:
        print("🔍 Obteniendo dato interesante...")
        res = requests.get("https://uselessfacts.jsph.pl/random.json?language=es")
        print(f"⚠️ Respuesta de la API: {res.text}")  # Mostrar el cuerpo de la respuesta

        if res.status_code == 200:
            dato_json = res.json()
            print(f"✅ Dato JSON recibido: {dato_json}")  # Mostrar el JSON completo
            texto_original = dato_json.get("text", None)
            if texto_original:
                traducido = GoogleTranslator(source='auto', target='es').translate(texto_original)
                print(f"✅ Dato obtenido y traducido: {traducido}")
                return traducido
            else:
                print("⚠️ No se encontró el campo 'text' en la respuesta.")
                return None
        else:
            print(f"⚠️ Error en la API de datos. Código: {res.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error al obtener el dato: {e}")
        return None

# Publicar un tweet
def publicar_tweet():
    if not client:
        print("⚠️ Cliente de Twitter no disponible. Tweet no publicado.")
        return

    dato = obtener_dato_interesante()
    if dato:
        try:
            response = client.create_tweet(text=f"Dato del Día: {dato}")
            tweet_id = response.data['id']
            print(f"✅ Tweet publicado con ID: {tweet_id}")
        except Exception as e:
            print(f"❌ Error al publicar el tweet: {e}")
    else:
        print("⚠️ No se obtuvo ningún dato para publicar.")

# Iniciar programador de tareas
def iniciar_scheduler():
    print("🕒 Iniciando programador de tweets cada 2 minutos...")
    publicar_tweet()  # Publicar un primer tweet al inicio
    schedule.every(2).minutes.do(publicar_tweet)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Flask App
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot activo y funcionando."

# Ejecutar servidor Flask y programador
if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 10000))

    scheduler_thread = threading.Thread(target=iniciar_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    print(f"🚀 Servidor Flask iniciado en el puerto {puerto}")
    app.run(host="0.0.0.0", port=puerto)
