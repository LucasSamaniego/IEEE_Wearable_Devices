from oled_utils import init_display, draw_triangle_on_display
import time

disp, image, draw = init_display()

directions = ["frente", "tras", "esquerda", "direita"]
for d in directions:
    draw_triangle_on_display(disp, draw, image, d)
    time.sleep(3)
