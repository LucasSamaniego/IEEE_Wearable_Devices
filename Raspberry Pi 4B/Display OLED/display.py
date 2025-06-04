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
import traceback
from waveshare_OLED import OLED_0in96
from PIL import Image, ImageDraw, ImageFont
logging.basicConfig(level=logging.DEBUG)

def draw_triangle(draw, direction, width, height):
    """Desenha um triângulo indicando a direção especificada"""
    if direction == "frente":
        # Triângulo apontando para cima
        points = [(width // 2, 0), (0, height), (width, height)]
    elif direction == "tras":
        # Triângulo apontando para baixo
        points = [(0, 0), (width, 0), (width // 2, height)]
    elif direction == "esquerda":
        # Triângulo apontando para a esquerda
        points = [(0, height // 2), (width, 0), (width, height)]
    elif direction == "direita":
        # Triângulo apontando para a direita
        points = [(0, 0), (width, height // 2), (0, height)]
    else:
        raise ValueError("Direção inválida: {}".format(direction))
    
    draw.polygon(points, fill=0)

try:
    disp = OLED_0in96.OLED_0in96()

    logging.info("\r 0.96inch OLED - Triângulos de Direção")
    # Initialize library.
    disp.Init()
    # Clear display.
    logging.info("Limpar display")
    disp.clear()

    # Cria imagem em branco para desenhar
    image = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image)

    # Lista das direções que queremos mostrar
    direcoes = ["frente", "tras", "esquerda", "direita"]

    for direcao in direcoes:
        logging.info(f"Desenhando triângulo para: {direcao}")
        # Limpa a imagem para cada novo desenho
        draw.rectangle((0, 0, disp.width, disp.height), fill=1)

        # Desenha triângulo
        draw_triangle(draw, direcao, disp.width, disp.height)

        # Mostra a imagem no display
        disp.ShowImage(disp.getbuffer(image))
        time.sleep(3)

    # Finaliza limpando o display
    disp.clear()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    disp.module_exit()
    exit()
