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
from PIL import Image,ImageDraw,ImageFont
logging.basicConfig(level=logging.DEBUG)

try:
    disp = OLED_0in96.OLED_0in96()

    logging.info("\r 0.96inch OLED ")
    # Initialize library.
    disp.Init()
    # Clear display.
    logging.info("clear display")
    disp.clear()
    
    # Create blank image for drawing.
    image1 = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    font1 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 30)
    #font2 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    logging.info ("Desenhando linha...")    
    draw.line([(0,0),(127,0)], fill = 0)
    draw.line([(0,63),(127,63)], fill = 0)
    draw.line([(127,0),(127,63)], fill = 0)
    logging.info ("Escrevendo texto...")
    draw.text((30,0), 'Direita ', font = font1, fill = 0)
    #draw.text((10,24), 'Samaniego', font = font1, fill = 0)
    image1 = image1.rotate(0)
    disp.ShowImage(disp.getbuffer(image1))
    time.sleep(5)

    logging.info ("Desenhando imagem...")
    Himage2 = Image.new('1', (disp.width, disp.height), 255)  # 255: clear the frame
    bmp = Image.open(os.path.join(picdir, '0in96.bmp'))
    Himage2.paste(bmp, (0,0))
    Himage2=Himage2.rotate(0)
    disp.ShowImage(disp.getbuffer(Himage2))
    time.sleep(3)
    disp.clear()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    disp.module_exit()
    exit()