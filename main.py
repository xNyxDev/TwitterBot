import os
import tweepy
import time
import requests
from deep_translator import GoogleTranslator

def obtener_claves_api():
    """
    Obtiene las claves de la API de Twitter de las variables de entorno.
    """
    api_key = os.environ.get("API_KEY")
    api_secret = os.environ.get("API_SECRET")
    bearer_token = os.environ.get("BEARER_TOKEN")
    api_token = os.environ.get("API_TOKEN")
    api_token_secret = os.environ.get("API_TOKEN_SECRET")
    return api_key, api_secret, bearer_token, api_token, api_token_secret

def verificar_claves_api(api_key, api_secret, bearer_token, api_token, api_token_secret):
    """
    Verifica si todas las variables de entorno requeridas están configuradas.
    """
    if not all([api_key, api_secret, bearer_token, api_token, api_token_secret]):
        print("Error: Faltan una o más variables de entorno requeridas.")
        return False
    return True

def obtener_dato_curioso():
    """
    Obtiene un dato curioso de la API de Useless Facts y lo traduce al español.

    Returns:
        str: El dato curioso traducido al español, o None si ocurre un error.
    """
    try:
        # API de Useless Facts (Inglés)
        response = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")
        response.raise_for_status()
        data = response.json()
        texto_original = data.get("text")

        if texto_original:
            # Traducir el texto a español
            translator = GoogleTranslator(target='es')
            texto_traducido = translator.translate(texto_original)
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

def publicar_tweet(cliente, dato):
    """
    Publica un tweet con el dato curioso proporcionado.

    Args:
        cliente (tweepy.Client): El cliente de la API de Twitter.
        dato (str): El dato curioso que se va a publicar.
    """
    try:
        cliente.create_tweet(text="Dato del Día: " + dato)
        print("Tweet enviado con éxito")
    except Exception as e:
        print(f"Error al enviar el tweet: {e}")

def main():
    """
    Función principal que ejecuta el bot de Twitter.
    """
    api_key, api_secret, bearer_token, api_token, api_token_secret = obtener_claves_api()
    if not verificar_claves_api(api_key, api_secret, bearer_token, api_token, api_token_secret):
        return  # Termina la ejecución si faltan claves

    cliente = tweepy.Client(bearer_token, api_key, api_secret, api_token, api_token_secret)

    while True:
        dato = obtener_dato_curioso()
        if dato:
            publicar_tweet(cliente, dato)
        else:
            print("No se pudo obtener un dato curioso. No se enviará ningún tweet.")
        time.sleep(120)

if __name__ == "__main__":
    main()
