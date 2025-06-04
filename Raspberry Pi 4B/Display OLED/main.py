#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
# Ajuste os diretórios conforme sua estrutura
picdir = "/home/samaniego/OLED_Module_Code/RaspberryPi/python/pic"
libdir = "/home/samaniego/OLED_Module_Code/RaspberryPi/python/lib"
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import time
import paho.mqtt.client as mqtt
from PIL import Image, ImageDraw, ImageFont
logging.basicConfig(level=logging.INFO)

from oled_utils import init_display

logging.basicConfig(level=logging.DEBUG)

def draw_triangle_on_display(display, draw, image, direction):
    """
    Função externa para desenhar o triângulo no display.
    """
    width = display.width
    height = display.height
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    
    if direction == "up":
        points = [(width//2, 0), (0, height), (width, height)]
    elif direction == "down":
        points = [(0, 0), (width, 0), (width//2, height)]
    elif direction == "left":
        points = [(0, height//2), (width, 0), (width, height)]
    elif direction == "right":
        points = [(0, 0), (width, height//2), (0, height)]
    else:
        raise ValueError("Direção inválida.")
    
    draw.polygon(points, outline=255, fill=255)
    display.ShowImage(display.getbuffer(image))

class MqttOLEDClient:
    def __init__(self, broker, port=1883, client_id=None, username=None, password=None):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password

        # Inicializa o cliente MQTT
        self.client = mqtt.Client(client_id)
        if username and password:
            self.client.username_pw_set(username, password)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Inicializa display usando biblioteca externa
        self.display, self.image, self.draw = init_display()

    def on_connect(self, client, userdata, flags, rc):
        logging.info(f"Conectado ao broker MQTT com código: {rc}")
        client.subscribe("API/WAY")
        logging.info("Inscrito no tópico 'API/WAY'.")

    def on_message(self, client, userdata, msg):
        direction = msg.payload.decode().strip().lower()
        logging.info(f"Direção recebida: {direction}")

        try:
            # Chama a função externa para desenhar
            draw_triangle_on_display(self.display, self.draw, self.image, direction)
            time.sleep(3)
        except ValueError:
            # Se direção inválida, mostrar texto de erro
            font = ImageFont.load_default()
            self.draw.rectangle((0, 0, self.display.width, self.display.height), fill=1)
            self.draw.text((10, 20), "Direção inválida", font=font, fill=0)
            self.display.ShowImage(self.display.getbuffer(self.image))

    def connect_and_loop(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()
        logging.info("Aguardando mensagens... (Ctrl+C para sair)")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Desconectando...")
            self.client.loop_stop()
            self.client.disconnect()
            self.display.clear()
            logging.info("Desconectado e display limpo.")

if __name__ == "__main__":
    mqtt_broker = "192.168.18.16"  # Ajuste para o IP do seu broker
    mqtt_port = 1883
    mqtt_client_id = "raspberry_pi_oled_client"

    mqtt_oled_client = MqttOLEDClient(mqtt_broker, mqtt_port, mqtt_client_id)
    mqtt_oled_client.connect_and_loop()
