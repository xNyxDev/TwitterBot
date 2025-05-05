import os
import tweepy
import time
import requests

def obtener_texto_de_json():
    """
    Obtiene el texto de un JSON de la API de Useless Facts.

    Returns:
        str: El texto extraído del JSON, o None si ocurre un error.
    """
    try:
        # API de Useless Facts (Inglés)
        response = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")
        response.raise_for_status()
        data = response.json()
        texto = data.get("text")  # Obtiene el valor del campo "text"

        if texto:
            return texto
        else:
            print("Error: La respuesta JSON no contiene el campo 'text'.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el texto del JSON: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

def publicar_tweet(texto):
    """
    Publica un tweet con el texto proporcionado.

    Args:
        texto (str): El texto que se va a publicar.
    """
    try:
        # Autenticación con la API de Twitter usando las variables de entorno
        client = tweepy.Client(
            bearer_token=os.environ.get("BEARER_TOKEN"),
            consumer_key=os.environ.get("API_KEY"),
            consumer_secret=os.environ.get("API_SECRET"),
            access_token=os.environ.get("API_TOKEN"),
            access_token_secret=os.environ.get("API_TOKEN_SECRET"),
        )
        client.create_tweet(text=texto)
        print("Tweet enviado con éxito")
    except Exception as e:
        print(f"Error al enviar el tweet: {e}")

def main():
    """
    Función principal que ejecuta el bot de Twitter.
    """
    while True:
        texto = obtener_texto_de_json()
        if texto:
            publicar_tweet("Daily Fact: " + texto)
        else:
            print("No se pudo obtener el texto del JSON. No se enviará ningún tweet.")
        time.sleep(360)

if __name__ == "__main__":
    main()
