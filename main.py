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

print(f"API_KEY: {API_KEY}")
print(f"API_SECRET: {API_SECRET}")
print(f"BEARER_TOKEN: {BEARER_TOKEN}")
print(f"API_TOKEN: {API_TOKEN}")
print(f"API_TOKEN_SECRET: {API_TOKEN_SECRET}")


app = Flask(__name__)
try:
    client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET, API_TOKEN, API_TOKEN_SECRET)
    print("Cliente de Twitter inicializado con éxito.")
except Exception as e:
    print(f"Error al inicializar el cliente de Twitter: {e}")
    client = None # Asegurarse de que client esté definido incluso en caso de error

def obtener_datos_interesantes():
    try:
        print("Intentando obtener un dato interesante...")
        res = request.get("https://uselessfacts.jsph.pl/random.json?language=es")
        print(f"Respuesta de la API de datos: {res.status_code}")
        if res.status_code == 200:
            dato_json = res.json()
            print(f"Datos JSON recibidos: {dato_json}")
            traducido = GoogleTranslator(source='auto', target='es').translate(dato_json.get("text"))
            print(f"Dato traducido: {traducido}")
            return traducido
        else:
            print(f"Error al obtener datos interesantes. Código de estado: {res.status_code}")
            return None
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return None

def publicar_tweet():
    if client: # Verificar si el cliente de Twitter se inicializó correctamente
        dato = obtener_datos_interesantes()
        if dato:
            print(f"Intentando publicar el dato: '{dato}'")
            try:
                response = client.create_tweet(text="Dato del Dia: " + dato)
                print(f"Tweet enviado con éxito. ID del tweet: {response.data['id']}")
            except Exception as e:
                print(f"Error al enviar el tweet: {e}")
        else:
            print("No se obtuvo un dato para publicar.")
    else:
        print("El cliente de Twitter no está inicializado. No se puede publicar el tweet.")

schedule.every().hour.do(publicar_tweet)

@app.route("/")
def hello():
    return "Hola, mundo!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    # Ejecutar el scheduler en un hilo separado para no bloquear la app Flask
    import threading
    def run_scheduler():
        print("Iniciando el scheduler de tweets...")
        while True:
            schedule.run_pending()
            time.sleep(1)

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    print(f"Aplicación Flask iniciada en el puerto: {port}")
    app.run(host="0.0.0.0", port=port)
