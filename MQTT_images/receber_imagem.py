import paho.mqtt.client as mqtt
import base64
from PIL import Image
import io

# Configurações do MQTT
BROKER = "192.168.18.16"  # Insira o endereço do seu broker MQTT
PORT = 1883
TOPIC = "imagem/mqtt"

# Função para processar e salvar a imagem recebida
def salvar_imagem(img_base64, output_path="imagem_recebida.jpg"):
    try:
        # Decodificar a imagem base64
        img_bytes = base64.b64decode(img_base64)
        img = Image.open(io.BytesIO(img_bytes))
        
        # Salvar a imagem no formato .jpg
        img.convert("RGB").save(output_path, "JPEG")
        print(f"Imagem salva em: {output_path}")
    except Exception as e:
        print(f"Erro ao salvar imagem: {e}")

# Callback executado quando uma mensagem é recebida
def on_message(client, userdata, msg):
    print("Mensagem recebida no tópico:", msg.topic)
    salvar_imagem(msg.payload.decode("utf-8"))

# Configuração do cliente MQTT
client = mqtt.Client()
client.on_message = on_message

# Conectar ao broker e subscrever ao tópico
client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC)

# Loop do cliente MQTT em uma thread separada
client.loop_start()

# Aguarde para receber imagens
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Encerrando...")
    client.loop_stop()
    client.disconnect()
