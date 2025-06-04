from oled_utils import init_display, draw_triangle_on_display
import time
import logging

logging.info("Tentando desenhar")
disp, image, draw = init_display()

directions = ["frente", "tras", "esquerda", "direita"]
dir = "frente"
draw_triangle_on_display(disp, draw, image, dir)
time.sleep(3)
