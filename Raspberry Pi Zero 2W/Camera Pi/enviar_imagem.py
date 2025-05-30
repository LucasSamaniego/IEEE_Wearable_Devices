import paho.mqtt.client as mqtt
import base64

# Configurações do MQTT
BROKER = "192.168.18.16"  # Insira o endereço do seu broker MQTT
PORT = 1883
TOPIC = "imagem/mqtt"

# Função para enviar uma imagem
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

# Enviar uma imagem
caminho_imagem = "foto2.jpg"  # Insira o caminho da imagem a ser enviada
enviar_imagem(client, caminho_imagem)

# Aguardar envio e finalizar conexão
import time
time.sleep(2)  # Tempo para garantir que o envio seja concluído antes de desconectar
client.loop_stop()
client.disconnect()