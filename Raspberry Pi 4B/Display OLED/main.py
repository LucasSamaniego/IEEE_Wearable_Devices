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
import traceback
import threading
import paho.mqtt.client as mqtt
from PIL import Image, ImageDraw, ImageFont
from waveshare_OLED import OLED_0in96

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

        # Inicializa o display OLED
        self.display = OLED_0in96.OLED_0in96()
        self.display.Init()
        self.display.clear()

        # Mostra a mensagem inicial
        self.init_display()

    def init_display(self):
        """Mostra 'Modo navegação' ao iniciar."""
        image = Image.new('1', (self.display.width, self.display.height), 255)
        draw = ImageDraw.Draw(image)

        font = ImageFont.load_default()
        text = "Modo navegação"
        w, h = draw.textsize(text, font=font)
        x = (self.display.width - w) // 2
        y = (self.display.height - h) // 2
        draw.text((x, y), text, font=font, fill=0)

        self.display.ShowImage(self.display.getbuffer(image))

    def on_connect(self, client, userdata, flags, rc):
        print(f"Conectado ao broker MQTT com código: {rc}")
        client.subscribe("API/WAY")
        print("Inscrito no tópico 'API/WAY'.")

    def on_message(self, client, userdata, msg):
        """Desenha o triângulo da direção recebida."""
        direction = msg.payload.decode().strip().lower()
        print(f"Direção recebida: {direction}")
        self.display_direction(direction)

    def display_direction(self, direction):
        # Cria uma imagem em branco
        image = Image.new('1', (self.display.width, self.display.height), 255)
        draw = ImageDraw.Draw(image)

        if direction == 'frente':
            # Triângulo para cima
            draw.polygon([(64, 0), (0, 63), (127, 63)], fill=0)
        elif direction == 'tras':
            # Triângulo para baixo
            draw.polygon([(0, 0), (127, 0), (64, 63)], fill=0)
        elif direction == 'esquerda':
            # Triângulo para a esquerda
            draw.polygon([(0, 32), (127, 0), (127, 63)], fill=0)
        elif direction == 'direita':
            # Triângulo para a direita
            draw.polygon([(127, 32), (0, 0), (0, 63)], fill=0)
        else:
            # Texto de erro
            font = ImageFont.load_default()
            draw.text((10, 20), "Direção inválida", font=font, fill=0)

        self.display.ShowImage(self.display.getbuffer(image))

    def connect_and_loop(self):
        """Conecta ao broker e mantém o loop rodando para receber mensagens."""
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()
        print("Aguardando mensagens... (Ctrl+C para sair)")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Desconectando...")
            self.client.loop_stop()
            self.client.disconnect()
            self.display.clear()
            print("Desconectado e display limpo.")

if __name__ == "__main__":
    mqtt_broker = "192.168.18.16"  # Ajuste para o IP do seu broker
    mqtt_port = 1883
    mqtt_client_id = "raspberry_pi_oled_client"

    mqtt_oled_client = MqttOLEDClient(mqtt_broker, mqtt_port, mqtt_client_id)
    mqtt_oled_client.connect_and_loop()
