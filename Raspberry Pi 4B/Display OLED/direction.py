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

def draw_triangle_on_display(direction):
    """
    Desenha um triângulo na direção especificada no display OLED.
    :param direction: 'frente', 'tras', 'esquerda', ou 'direita'
    """
    try:
        # Inicializa o display
        disp = OLED_0in96.OLED_0in96()
        logging.info("\r0.96inch OLED - Triângulo Direcional")
        disp.Init()
        disp.clear()

        # Cria imagem em branco
        image = Image.new('1', (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image)

        # Escolhe os pontos do triângulo com base na direção
        width, height = disp.width, disp.height
        if direction == "frente":
            points = [(width // 2, 0), (0, height), (width, height)]
        elif direction == "tras":
            points = [(0, 0), (width, 0), (width // 2, height)]
        elif direction == "esquerda":
            points = [(0, height // 2), (width, 0), (width, height)]
        elif direction == "direita":
            points = [(0, 0), (width, height // 2), (0, height)]
        else:
            raise ValueError("Direção inválida: {}".format(direction))

        # Desenha o triângulo
        draw.polygon(points, fill=0)

        # Mostra no display
        disp.ShowImage(disp.getbuffer(image))
        logging.info(f"Triângulo para '{direction}' desenhado no display.")

    except IOError as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info("Interrompido pelo usuário (Ctrl+C).")
        disp.module_exit()
        exit()

# Exemplo de uso:
if __name__ == "__main__":
    import time
    for dir in ["frente", "tras", "esquerda", "direita"]:
        draw_triangle_on_display(dir)
        time.sleep(3)
