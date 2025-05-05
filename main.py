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

if not all([API_KEY, API_SECRET, BEARER_TOKEN, API_TOKEN, API_TOKEN_SECRET]):
    print("Error: Faltan una o más variables de entorno requeridas.")
    exit(1)

client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET, API_TOKEN, API_TOKEN_SECRET)

def obtener_datos_interesantes():
    try:
        res = request.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")
        if res.status_code == 200:
            data = res.json()
            dato_en = data.get("text")
            if dato_en:
                traducido = GoogleTranslator(source='en', target='es').translate(dato_en)
                return traducido
            else:
                print("Error: La respuesta JSON no contiene el campo 'text'.")
                return None
        else:
            print(f"Error al obtener datos interesantes. Código de estado: {res.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

while True:
    dato = obtener_datos_interesantes()
    if dato:
        try:
            client.create_tweet(text="Dato del Dia: " + dato)
            print("Tweet enviado con éxito")
        except Exception as e:
            print(f"Error al enviar el tweet: {e}")
    else:
        print("No se pudo obtener un dato interesante. No se enviará ningún tweet.")

    time.sleep(120)

if __name__ == "__main__":
    pass
