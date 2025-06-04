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

def init_display():
    disp = OLED_0in96.OLED_0in96()
    disp.Init()
    disp.clear()
    image = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image)
    return disp, image, draw

def draw_triangle_on_display(disp, draw, image, direction):
    width, height = disp.width, disp.height
    draw.rectangle((0, 0, width, height), fill=1)
    logging.info("Tentando desenhar")
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
    draw.polygon(points, fill=0)
    disp.ShowImage(disp.getbuffer(image))
