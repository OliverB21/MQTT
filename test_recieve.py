import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    mqttc.subscribe("myroom/temperature")

def on_message(client, userdata, msg):
    print("Received:", msg.payload.decode())

mqttc = mqtt.Client()
mqttc.connect("mqtt.eclipseprojects.io", 1883, 60)

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.loop_forever()