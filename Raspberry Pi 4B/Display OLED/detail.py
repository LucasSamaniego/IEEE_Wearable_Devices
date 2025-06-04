import paho.mqtt.client as mqtt
import threading

class MqttClient:
    def __init__(self, broker, port=1883, client_id=None, username=None, password=None):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password
        self.client = mqtt.Client(client_id)
        self.message_received = threading.Event()  # Evento para sincronização
        self.message = None

        # Configuração de autenticação, se fornecido
        if username and password:
            self.client.username_pw_set(username, password)

        # Definindo os callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        """Callback quando o cliente se conecta ao broker."""
        print(f"Conectado com código de resultado {rc}")

    def on_message(self, client, userdata, msg):
        """Callback quando uma mensagem é recebida de um tópico inscrito."""
        self.message = msg.payload.decode()
        self.message_received.set()  # Sinaliza que uma mensagem foi recebida
        print(f"Mensagem recebida '{self.message}' no tópico '{msg.topic}'")

    def connect(self):
        """Conecta ao broker MQTT."""
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()  # Inicia o loop em um thread separado

    def subscribe(self, topic):
        """Inscreve o cliente em um tópico."""
        self.client.subscribe(topic)
        print(f"Inscrito no tópico '{topic}'")

    def publish(self, topic, message):
        """Publica uma mensagem em um tópico."""
        self.client.publish(topic, message)
        print(f"Mensagem '{message}' publicada no tópico '{topic}'")

    def disconnect(self):
        """Desconecta do broker MQTT."""
        self.client.loop_stop()  # Para o loop
        self.client.disconnect()
        print("Desconectado do broker MQTT")

def conect_broker():
    mqtt_broker = "192.168.18.16"  # Altere para o endereço do seu broker MQTT
    mqtt_port = 1883  # Altere se o broker usar uma porta diferente
    mqtt_client_id = "raspberry_pi_client"  # Opcional
    mqtt_username = None  # Altere se seu broker exigir autenticação
    mqtt_password = None  # Altere se seu broker exigir autenticação

    client = MqttClient(mqtt_broker, mqtt_port, mqtt_client_id, mqtt_username, mqtt_password)
    client.connect()
    return client

def solicitar(item):
    client = conect_broker()  # Conecta o cliente ao broker MQTT
    try:
        client.publish("detail/item/publish", item)
    except KeyboardInterrupt:
        print("Interrompido pelo usuário")
    finally:
        client.disconnect()

def receber(timeout=10):
    client = conect_broker()  # Conecta o cliente ao broker MQTT
    client.subscribe("API/WAY")

    # Espera por uma mensagem por um tempo especificado
    client.message_received.wait(timeout)

    message = client.message
    client.disconnect()

    if message:
        return message
    else:
        return "Informação não recebida"

