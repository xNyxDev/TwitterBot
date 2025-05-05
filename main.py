import os
import tweepy
import time
import requests
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
    exit(1)

client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET, API_TOKEN, API_TOKEN_SECRET)

def obtener_dato_curioso():
    """
    Obtiene un dato curioso de una API externa y lo traduce al español.

    Returns:
        str: El dato curioso traducido al español, o None si ocurre un error.
    """
    try:
        # API de Chukcha (Ruso)
        response = requests.get("https://jokes.шутники.рф/random_joke")
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
        data = response.json()
        joke_text_ru = data.get("text")

        if joke_text_ru:
            # Traducir de Ruso a Español
            translator = GoogleTranslator(source='ru', target='es')
            joke_text_es = translator.translate(joke_text_ru)
            return joke_text_es
        else:
            print("Error: La respuesta JSON no contiene el campo 'text'.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el dato curioso: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

def publicar_tweet(dato):
    try:
        client.create_tweet(text="Dato del Día: " + dato)
        print("Tweet enviado con éxito")
    except Exception as e:
        print(f"Error al enviar el tweet: {e}")

if __name__ == "__main__":
    while True:
        dato = obtener_dato_curioso()
        if dato:
            publicar_tweet(dato)
        else:
            print("No se pudo obtener un dato curioso. No se enviará ningún tweet.")
        time.sleep(120)
