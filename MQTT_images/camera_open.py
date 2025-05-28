import paho.mqtt.client as mqtt
import cv2
from picamera2 import Picamera2
from pyzbar.pyzbar import decode

# Configurações do MQTT
BROKER = "192.168.18.16"  # Insira o endereço do seu broker MQTT
PORT = 1883
TOPIC = "qrcode/mqtt"

# Função para enviar mensagens via MQTT
def enviar_mensagem(client, mensagem):
    try:
        # Publicar a mensagem no tópico MQTT
        result = client.publish(TOPIC, mensagem)
        result.wait_for_publish()
        print(f"Mensagem enviada: {mensagem}")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

# Inicializar o cliente MQTT
client = mqtt.Client()
client.connect(BROKER, PORT, 60)

# Iniciar loop MQTT
client.loop_start()

# Inicializar a câmera
picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)
picam2.start()

try:
    print("Câmera aberta. Identificando QR Codes... (Pressione Ctrl+C para sair)")
    while True:
        # Capturar um frame da câmera
        frame = picam2.capture_array()

        # Identificar QR Codes no frame
        decoded_objects = decode(frame)
        for obj in decoded_objects:
            qr_data = obj.data.decode("utf-8")
            print(f"QR Code detectado: {qr_data}")
            
            # Enviar a informação do QR Code via MQTT
            enviar_mensagem(client, qr_data)

except KeyboardInterrupt:
    print("Encerrando execução.")

finally:
    # Finalizar recursos
    picam2.close()
    client.loop_stop()
    client.disconnect()
