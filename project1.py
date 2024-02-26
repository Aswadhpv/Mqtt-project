
import os
import subprocess
import configparser
import socket
import paho.mqtt.client as mqtt

# Load config from external file
config = configparser.ConfigParser()
config.read('config.ini')

# MQTT Settings
mqtt_broker_address = config.get('MQTT', 'broker_address')
mqtt_topic_volume = config.get('MQTT', 'topic_volume')
mqtt_topic_message = config.get('MQTT', 'topic_message')

# UDP Settings
udp_server_address = config.get('UDP', 'server_address')
udp_server_port = config.getint('UDP', 'server_port')

# ALSA Settings
alsa_device = "default"  # You may need to change this according to your setup

def adjust_volume(volume):
    # Adjust volume using ALSA
    command = ['amixer', '-D', alsa_device, 'sset', 'Master', f'{volume}%']
    subprocess.run(command, check=True)

def send_udp_message(message):
    # Send message via UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message.encode('koi8-r'), (udp_server_address, udp_server_port))

def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode('utf-8')

    # Process messages based on topic
    if topic == mqtt_topic_volume:
        volume = int(payload)
        adjust_volume(volume)
        print(f"Adjusted volume to {volume}%")

    elif topic == mqtt_topic_message:
        send_udp_message(payload)
        print(f"Sent message via UDP: {payload}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe([(mqtt_topic_volume, 0), (mqtt_topic_message, 0)])
    else:
        print(f"Failed to connect to MQTT Broker with return code {rc}")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT Broker")

if __name__ == "__main__":
    # MQTT Setup
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_disconnect = on_disconnect

    mqtt_client.connect(mqtt_broker_address, 1883, 60)
    mqtt_client.loop_forever()
