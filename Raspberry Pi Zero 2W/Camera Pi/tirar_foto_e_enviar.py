import paho.mqtt.client as mqtt
import base64
import cv2
from picamera2 import Picamera2
import os
import time

# Configurações do MQTT
BROKER = "192.168.18.16"  # Insira o endereço do seu broker MQTT
PORT = 1883
TOPIC = "imagem/mqtt"

# Configuração do caminho para salvar a foto temporariamente
TEMP_IMAGE_PATH = "/tmp/captured_image.jpg"

# Função para capturar uma imagem usando Picamera2 e OpenCV
def capturar_imagem(caminho_imagem):
    try:
        # Inicializar a câmera
        picam2 = Picamera2()
        picam2.start()
        time.sleep(2)  # Permitir ajuste de foco e exposição
        
        # Capturar imagem
        frame = picam2.capture_array()
        
        # Salvar a imagem capturada
        cv2.imwrite(caminho_imagem, frame)
        print(f"Imagem capturada: {caminho_imagem}")
        
        # Liberar a câmera e fechar janelas
        picam2.close()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Erro ao capturar imagem: {e}")

# Função para enviar uma imagem via MQTT
def enviar_imagem(client, imagem_caminho):
    try:
        # Ler a imagem e converter para base64
        with open(imagem_caminho, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode("utf-8")
        
        # Publicar a imagem codificada no tópico MQTT
        result = client.publish(TOPIC, img_base64)
        result.wait_for_publish()
        print(f"Imagem enviada: {imagem_caminho}")
    except Exception as e:
        print(f"Erro ao enviar imagem: {e}")

# Configuração do cliente MQTT
client = mqtt.Client()

# Conectar ao broker MQTT
client.connect(BROKER, PORT, 60)

# Iniciar loop MQTT
client.loop_start()

# Capturar uma imagem
capturar_imagem(TEMP_IMAGE_PATH)

# Enviar a imagem capturada
enviar_imagem(client, TEMP_IMAGE_PATH)

# Remover a imagem temporária para liberar espaço
if os.path.exists(TEMP_IMAGE_PATH):
    os.remove(TEMP_IMAGE_PATH)
    print(f"Imagem temporária removida: {TEMP_IMAGE_PATH}")

# Aguardar envio e finalizar conexão
time.sleep(2)  # Tempo para garantir que o envio seja concluído antes de desconectar
client.loop_stop()
client.disconnect()
