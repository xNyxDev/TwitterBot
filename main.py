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
    """
    Obtiene un dato aleatorio. Maneja posibles errores durante la solicitud
    y el proceso de traducción. Incluye un valor de retorno por defecto.

    Devuelve:
        str: Un dato aleatorio traducido, o None si ocurre un error.
    """
    try:
        res = request.get("https://uselessfacts.jsph.pl/random.json?language=en") #cambio el language a en
        res.raise_for_status()  # Lanza una excepción para códigos de estado incorrectos (4xx o 5xx)

        data = res.json()  # Parsea los datos JSON
        if "text" in data:
            traducido = GoogleTranslator(source='en', target='es').translate(data["text"]) #agrego la traduccion
            return traducido # Devuelve el texto traducido
        else:
            print("Error: la clave \'text\' no se encontró en la respuesta de la API.")
            return None # Devuelve explícitamente None en caso de que falte la clave 'text'
    except request.exceptions.RequestException as e:
        print(f"Error al obtener los datos: {e}")
        return None
    except Exception as e:
        print(f"Error al traducir los datos: {e}")
        return None

def main(): # Se agregó una función main
    """
    Función principal para obtener y tuitear un dato aleatorio cada hora.
    """
    while True:
        dato = obtener_datos_interesantes()
        if dato: # Verifica que dato no sea None
            try:
                client.create_tweet(text="Dato del Dia: " + dato)
                print("Tweet enviado con éxito")
            except tweepy.TweepyException as e:
                print(f"Error al enviar el tweet: {e}")
        else:
            print("No se pudo obtener un dato interesante. No se enviará el tweet.")

        time.sleep(3600)  # Espera 1 hora antes de enviar el siguiente tweet

if __name__ == "__main__":
    main()
