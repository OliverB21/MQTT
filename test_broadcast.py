import time
import paho.mqtt.client as mqtt
import random

mqttc = mqtt.Client()
mqttc.connect("mqtt.eclipseprojects.io", 1883, 60)

if __name__ == "__main__":
    print("Publishing...")
    
    while True:
        temperature = random.randint(20,30)
        humidity = random.randint(20,90)
        co2 = random.randint(300,400)
        mqttc.publish("ooffice/temperature", temperature)
        mqttc.publish("ooffice/humidity", humidity)
        mqttc.publish("ooffice/co2", co2)
        time.sleep(2)