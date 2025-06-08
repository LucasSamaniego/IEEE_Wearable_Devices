import cv2
from picamera2 import Picamera2

# Inicializar a câmera
picam2 = Picamera2()
picam2.start()

# Capturar imagem
frame = picam2.capture_array()

# Salvar a imagem capturada
cv2.imwrite("imagem.jpg", frame)

# Liberar a câmera e fechar janelas
picam2.close()
cv2.destroyAllWindows()
