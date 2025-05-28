import paho.mqtt.client as mqtt
import time

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "raspi/signal"
CLIENT_ID = "pub"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, CLIENT_ID)

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Подключенно с кодом: {reason_code}")

client.on_connect = on_connect
client.connect(BROKER, PORT)
client.loop_start()

def pub(signal):
    try:
        client.publish(TOPIC, str(signal), qos=1)
        print(f"Отправлен сигнал: {signal}")
        time.sleep(0.2)
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()