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
        # API de Useless Facts (Inglés)
        response = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")
        response.raise_for_status()
        data = response.json()
        joke_text = data.get("text")

        if joke_text:
            # Traducir el texto a español
            translator = GoogleTranslator(target='es')
            texto_traducido = translator.translate(joke_text)
            return texto_traducido
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
    """
    Publica un tweet con el dato curioso proporcionado.

    Args:
        dato (str): El dato curioso que se va a publicar.
    """
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
