import tweepy
import time
import os
import requests as request
import schedule

from deep_translator import GoogleTranslator
from flask import Flask

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
API_TOKEN = os.environ.get("API_TOKEN")
API_TOKEN_SECRET = os.environ.get("API_TOKEN_SECRET")

app = Flask(__name__)
client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET, API_TOKEN, API_TOKEN_SECRET)

def obtener_datos_interesantes():
    try:
        res = request.get("https://uselessfacts.jsph.pl/random.json?language=es")
        if res.status_code == 200:
            traducido = GoogleTranslator(source='auto', target='es').translate(res.json().get("text"))
            return traducido
        else:
            print("Error al obtener datos interesantes")
    except Exception as e:
        print(f"Error: {e}")
        return None

def publicar_tweet():
    dato = obtener_datos_interesantes()
    if dato:
        try:
            client.create_tweet(text="Dato del Dia: " + dato)
            print("Tweet enviado con éxito")
        except Exception as e:
            print(f"Error al enviar el tweet: {e}")

schedule.every().hour.do(publicar_tweet)

@app.route("/")
def hello():
    return "Hola, mundo!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    # Ejecutar el scheduler en un hilo separado para no bloquear la app Flask
    import threading
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    app.run(host="0.0.0.0", port=port)
