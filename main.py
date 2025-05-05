import os
import tweepy
import time
import requests as request
from deep_translator import GoogleTranslator

API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
API_TOKEN = os.environ.get("API_TOKEN")
API_TOKEN_SECRET = os.environ.get("API_TOKEN_SECRET")

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

while True:
    dato = obtener_datos_interesantes()
    try:
        client.create_tweet(text="Dato del Dia: " + dato)
        print("Tweet enviado con éxito")
    except Exception as e:
        print(f"Error al enviar el tweet: {e}")

    time.sleep(3600)  # Espera 1 hora antes de enviar el siguiente tweet
