#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
import logging
import time
import traceback
import threading
import paho.mqtt.client as mqtt
from PIL import Image, ImageDraw
from waveshare_OLED import OLED_0in96

# Ajuste os diretórios conforme sua estrutura
picdir = "/home/samaniego/OLED_Module_Code/RaspberryPi/python/pic"
libdir = "/home/samaniego/OLED_Module_Code/RaspberryPi/python/lib"
if os.path.exists(libdir):
    sys.path.append(libdir)

logging.basicConfig(level=logging.DEBUG)

# ------------------------------
# CLASSE PARA DESENHAR TRIÂNGULOS
# ------------------------------

def draw_triangle(draw, direction, width, height):
    """Desenha um triângulo apontando na direção especificada."""
    if direction == "frente":
        points = [(width // 2, 0), (0, height), (width, height)]
    elif direction == "trás":
        points = [(0, 0), (width, 0), (width // 2, height)]
    elif direction == "esquerda":
        points = [(0, height // 2), (width, 0), (width, height)]
    elif direction == "direita":
        points = [(0, 0), (width, height // 2), (0, height)]
    else:
        # Se a direção for inválida, desenha um X para indicar erro
        draw.line([(0, 0), (width, height)], fill=0, width=3)
        draw.line([(0, height), (width, 0)], fill=0, width=3)
        return
    
    draw.polygon(points, fill=0)

# --------------------------------
# CLASSE MQTT INTEGRADA COM DISPLAY
# --------------------------------

class MqttDisplayClient:
    def __init__(self, broker, port=1883, topic="API/WAY", client_id=None, username=None, password=None):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_id = client_id
        self.username = username
        self.password = password
        self.client = mqtt.Client(client_id)
        
        # Inicializa display OLED
        self.disp = OLED_0in96.OLED_0in96()
        self.disp.Init()
        self.disp.clear()
        logging.info("Display OLED inicializado.")
        
        # Configuração de autenticação MQTT
        if username and password:
            self.client.username_pw_set(username, password)
        
        # Callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print(f"[MQTT] Conectado com código: {rc}")
        self.client.subscribe(self.topic)
        print(f"[MQTT] Inscrito no tópico: {self.topic}")

    def on_message(self, client, userdata, msg):
        """Callback executado ao receber mensagem do tópico."""
        direction = msg.payload.decode().strip().lower()
        print(f"[MQTT] Mensagem recebida: '{direction}'")

        # Desenhar triângulo correspondente
        self.display_direction(direction)

    def display_direction(self, direction):
        """Desenha no display OLED a direção recebida."""
        image = Image.new('1', (self.disp.width, self.disp.height), "WHITE")
        draw = ImageDraw.Draw(image)
        
        # Desenha o triângulo correspondente
        draw_triangle(draw, direction, self.disp.width, self.disp.height)
        
        # Mostra no display
        self.disp.ShowImage(self.disp.getbuffer(image))

    def connect_and_loop(self):
        """Conecta ao broker e inicia o loop de escuta."""
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_forever()

# ------------------------------
# FUNÇÃO PRINCIPAL
# ------------------------------

def main():
    mqtt_broker = "192.168.18.16"  # Ajuste para o seu broker
    mqtt_port = 1883
    mqtt_topic = "API/WAY"
    
    # Inicializa cliente MQTT com OLED
    mqtt_oled_client = MqttDisplayClient(mqtt_broker, mqtt_port, mqtt_topic)
    
    try:
        mqtt_oled_client.connect_and_loop()
    except KeyboardInterrupt:
        print("Interrompido pelo usuário (Ctrl+C).")
        mqtt_oled_client.disp.clear()
        mqtt_oled_client.client.loop_stop()
        mqtt_oled_client.client.disconnect()

if __name__ == "__main__":
    main()
