import os
import subprocess
import json
import socket
import paho.mqtt.client as mqtt
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Config file 'config.json' not found.")
        return None
    except json.JSONDecodeError:
        logger.error("Error decoding JSON from config file.")
        return None

def adjust_volume(volume, alsa_device):
    try:
        # Adjust volume using ALSA
        command = ['amixer', '-D', alsa_device, 'sset', 'Master', f'{volume}%']
        subprocess.run(command, check=True)
        logger.info(f"Volume adjusted to {volume}%")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error adjusting volume: {e}")

def send_udp_message(message, udp_server_address, udp_server_port):
    try:
        # Send message via UDP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(message.encode('koi8-r'), (udp_server_address, udp_server_port))
        logger.info(f"Message sent via UDP: {message}")
    except Exception as e:
        logger.error(f"Error sending UDP message: {e}")

def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode('utf-8')

    # Process messages based on topic
    if topic == config['mqtt']['topic_volume']:
        volume = int(payload)
        adjust_volume(volume, config['alsa']['device'])

    elif topic == config['mqtt']['topic_message']:
        send_udp_message(payload, config['udp']['server_address'], config['udp']['server_port'])

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT Broker")
        client.subscribe([(config['mqtt']['topic_volume'], 0), (config['mqtt']['topic_message'], 0)])
    else:
        logger.error(f"Failed to connect to MQTT Broker with return code {rc}")

def on_disconnect(client, userdata, rc):
    logger.warning("Disconnected from MQTT Broker")

if __name__ == "__main__":
    # Load config
    config = load_config()
    if not config:
        exit(1)

    # MQTT Setup
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.on_disconnect = on_disconnect

    try:
        mqtt_client.connect(config['mqtt']['broker_address'], 1883, 60)
        mqtt_client.loop_forever()
    except Exception as e:
        logger.error(f"Error connecting to MQTT Broker: {e}")
