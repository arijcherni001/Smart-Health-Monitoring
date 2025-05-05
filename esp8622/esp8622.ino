#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Home";           // ⚠️ Ton SSID WiFi
const char* password = "wifi123"; // ⚠️ Ton mot de passe WiFi
const char* mqtt_server = "broker.hivemq.com"; // Serveur MQTT HiveMQ

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println("Connexion au WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnecté au WiFi");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Connexion MQTT...");
    if (client.connect("ESP8266Client")) {
      Serial.println("connecté au broker");
      // Tu peux t'abonner ici si tu veux recevoir des messages
      // client.subscribe("esp8266/topic");
    } else {
      Serial.print("Échec, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(9600);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Exemple d'envoi de message simple
  String payload = "Bonjour depuis ESP8266";
  client.publish("esp8266/test", payload.c_str());
  Serial.println("Message envoyé : " + payload);

  delay(5000);
}
