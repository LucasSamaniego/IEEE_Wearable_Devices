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

def draw_triangle_on_display(disp, draw, image, direction):
    """
    Desenha um triângulo na direção especificada no display OLED.
    :param disp: objeto do display inicializado
    :param draw: objeto ImageDraw associado à imagem
    :param image: objeto PIL Image
    :param direction: 'frente', 'tras', 'esquerda' ou 'direita'
    """
    width, height = disp.width, disp.height

    # Limpa a imagem antes de desenhar (fundo branco)
    draw.rectangle((0, 0, width, height), fill=1)

    if direction == "frente":
        points = [(width // 2, 0), (0, height), (width, height)]
    elif direction == "tras":
        points = [(0, 0), (width, 0), (width // 2, height)]
    elif direction == "esquerda":
        points = [(0, height // 2), (width, 0), (width, height)]
    elif direction == "direita":
        points = [(0, 0), (width, height // 2), (0, height)]
    else:
        raise ValueError(f"Direção inválida: {direction}")

    # Desenha triângulo preto no fundo branco
    draw.polygon(points, fill=0)

    # Atualiza o display com a imagem desenhada
    disp.ShowImage(disp.getbuffer(image))
    logging.info(f"Triângulo para '{direction}' desenhado no display.")

if __name__ == "__main__":
    try:
        disp = OLED_0in96.OLED_0in96()
        logging.info("\r0.96inch OLED - Triângulos de Direção")
        disp.Init()
        disp.clear()

        # Cria imagem e contexto de desenho uma vez
        image = Image.new('1', (disp.width, disp.height), "WHITE")
        draw = ImageDraw.Draw(image)

        # Exemplo: desenhar triângulos para todas as direções
        directions = ["frente", "tras", "esquerda", "direita"]
        for direction in directions:
            logging.info(f"Desenhando triângulo para: {direction}")
            draw_triangle_on_display(disp, draw, image, direction)
            time.sleep(3)

        # Finaliza limpando o display
        disp.clear()

    except IOError as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info("Interrompido pelo usuário (Ctrl+C).")
        disp.module_exit()
        exit()
