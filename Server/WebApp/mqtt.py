import paho.mqtt.client as mqtt
import time

# Função para enviar uma imagem
def navegar(local):
    try:

        # Configurações do MQTT
        BROKER = "test.mosquitto.org"  # Insira o endereço do seu broker MQTT
        PORT = 1883
        TOPIC = "navegar"

        # Configuração do cliente MQTT
        client = mqtt.Client()

        # Conectar ao broker MQTT
        client.connect(BROKER, PORT, 60)

        # Iniciar loop MQTT
        client.loop_start()
        
        # Publicar a imagem codificada no tópico MQTT
        result = client.publish(TOPIC, local)
        result.wait_for_publish()
        print(f"Navegação iniciada")

        # Aguardar envio e finalizar conexão
        time.sleep(2)  # Tempo para garantir que o envio seja concluído antes de desconectar
        client.loop_stop()
        client.disconnect()
    
    except Exception as e:
        print(f"Erro ao iniciar navegação: {e}")