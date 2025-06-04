#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
import logging
import time
import paho.mqtt.client as mqtt
from PIL import Image, ImageDraw, ImageFont

# Ajuste os diretórios conforme sua estrutura
picdir = "/home/samaniego/OLED_Module_Code/RaspberryPi/python/pic"
libdir = "/home/samaniego/OLED_Module_Code/RaspberryPi/python/lib"
if os.path.exists(libdir):
    sys.path.append(libdir)

from oled_utils import init_display, draw_triangle_on_display

logging.basicConfig(level=logging.DEBUG)

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

        # Mostra mensagem inicial
        self.init_display_message()

    def init_display_message(self):
        font = ImageFont.load_default()
        text = "Modo navegação"
        w, h = self.draw.textsize(text, font=font)
        x = (self.display.width - w) // 2
        y = (self.display.height - h) // 2

        # Limpa antes de escrever
        self.draw.rectangle((0, 0, self.display.width, self.display.height), fill=1)
        self.draw.text((x, y), text, font=font, fill=0)
        self.display.ShowImage(self.display.getbuffer(self.image))

    def on_connect(self, client, userdata, flags, rc):
        logging.info(f"Conectado ao broker MQTT com código: {rc}")
        client.subscribe("API/WAY")
        logging.info("Inscrito no tópico 'API/WAY'.")

    def on_message(self, client, userdata, msg):
        direction = msg.payload.decode().strip().lower()
        logging.info(f"Direção recebida: {direction}")

        try:
            draw_triangle_on_display(self.display, self.draw, self.image, direction)
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
