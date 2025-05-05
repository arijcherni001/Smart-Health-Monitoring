import random
import paho.mqtt.client as mqtt
from django.utils.timezone import now
from .models import Data

# Paramètres MQTT
mqtt_broker = "broker.hivemq.com"
mqtt_topic = "esp8266/health"

# Fonction qui sera appelée lors de la connexion au broker
def on_connect(client, userdata, flags, rc):
    print(f"Connecté avec le code {rc}")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    # Parse les données JSON
    message = msg.payload.decode("utf-8")
    print("--------STM Received---------")
    print(f"Message reçu : {message}")

    # Enregistrer les données dans la base de données
    try:
        import json
        data = json.loads(message)
        
        temperature = data.get("temperature")
        oxygene = data.get("humidity")
        bpm = data.get("bpm")
        
        Data.objects.create(temperature=temperature, oxygene=oxygene, bpm=bpm, timestamp=now())
        print(f"Données enregistrées: Temp={temperature}, Oxygene={oxygene}, BPM={bpm}")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des données: {e}")

# Initialiser le client MQTT
def start_mqtt_consumer():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Se connecter au broker
    client.connect(mqtt_broker, 1883, 60)
    
    # Boucle infinie pour écouter les messages
    client.loop_forever()
