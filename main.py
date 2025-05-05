import tweepy
import time
import requests as request
from deep_translator import GoogleTranslator

API_KEY = "w8LLH56zq2xTfxmMkNnuJ7tMl"
API_SECRET = "XpHybmgDo2qVy6O6HFuf90NUEvaKL6FMCnBtJ1VfL8NLwZPHQn"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAADs%2F1AEAAAAAiKH4DHiJ9eHySkqME3ku2z2mlJI%3DbID8tRsmqgGC05gXjJ6xqa3CIG8RqqgqAngWeZEeAqIBdsP2Tn"
API_TOKEN = "1919411570901180416-2IGtHZ8Fv2MSzgrxcwg842iO9O7OoP"
API_TOKEN_SECRET = "GVMjYcz154uvIO5XTDnn1oScCoaSMLpBOr9rpxE4kXmWv"

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