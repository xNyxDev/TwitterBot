import os
import tweepy
import time
import requests as request
from deep_translator import GoogleTranslator

# Obtiene las claves de la API de las variables de entorno
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
API_TOKEN = os.environ.get("API_TOKEN")
API_TOKEN_SECRET = os.environ.get("API_TOKEN_SECRET")

# Verifica si todas las variables de entorno requeridas están configuradas
if not all([API_KEY, API_SECRET, BEARER_TOKEN, API_TOKEN, API_TOKEN_SECRET]):
    print("Error: Faltan una o más variables de entorno requeridas.")
    exit(1)  # Usa sys.exit(1) para una salida más limpia con código de error

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

    time.sleep(3)  # Espera 1 hora antes de enviar el siguiente tweet

if __name__ == "__main__":
    main()
