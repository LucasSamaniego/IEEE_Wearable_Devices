#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
picdir = "/home/samaniego/OLED_Module_Code/RaspberryPi/python/pic"
libdir = "/home/samaniego/OLED_Module_Code/RaspberryPi/python/lib"
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import time
from waveshare_OLED import OLED_0in96
from PIL import Image, ImageDraw

logging.basicConfig(level=logging.DEBUG)
# Configurações MQTT
MQTT_BROKER = "seu_broker_aqui"
MQTT_PORT = 1883
MQTT_TOPIC = "direcao/display"

def init_display():
    """Inicializa o display e retorna os objetos disp, image e draw"""
    disp = OLED_0in96.OLED_0in96()
    disp.Init()
    disp.clear()
    image = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image)
    return disp, image, draw

def draw_triangle(disp, image, draw, direction):
    """Desenha um triângulo apontando para a direção no display"""
    width, height = disp.width, disp.height
    draw.rectangle((0, 0, width, height), fill=1)  # Fundo branco

    if direction == "frente":
        points = [(width // 2, 0), (0, height), (width, height)]
    elif direction == "tras":
        points = [(0, 0), (width, 0), (width // 2, height)]
    elif direction == "esquerda":
        points = [(0, height // 2), (width, 0), (width, height)]
    elif direction == "direita":
        points = [(0, 0), (width, height // 2), (0, height)]
    else:
        logging.warning(f"Direção inválida recebida: {direction}")
        return  # Não atualiza display se direção inválida

    draw.polygon(points, fill=0)
    disp.ShowImage(disp.getbuffer(image))
    logging.info(f"Triângulo para '{direction}' desenhado no display.")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Conectado ao broker MQTT com sucesso")
        client.subscribe(MQTT_TOPIC)
        logging.info(f"Inscrito no tópico {MQTT_TOPIC}")
    else:
        logging.error(f"Falha ao conectar, código de retorno: {rc}")

def on_message(client, userdata, msg):
    direction = msg.payload.decode().strip().lower()
    logging.info(f"Mensagem recebida no tópico {msg.topic}: {direction}")
    draw_triangle(userdata['disp'], userdata['image'], userdata['draw'], direction)

def main():
    disp, image, draw = init_display()

    # Exibe mensagem inicial
    draw.rectangle((0, 0, disp.width, disp.height), fill=1)
    from PIL import ImageFont
    font = ImageFont.load_default()
    draw.text((0, disp.height//2 - 8), "Modo navegação", font=font, fill=0)
    disp.ShowImage(disp.getbuffer(image))

    # Configura MQTT
    client = mqtt.Client(userdata={'disp': disp, 'image': image, 'draw': draw})
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
    except Exception as e:
        logging.error(f"Erro conectando ao broker MQTT: {e}")
        return

    client.loop_forever()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Interrompido pelo usuário, saindo...")
