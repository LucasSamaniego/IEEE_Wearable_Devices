from oled_utils import init_display, draw_triangle_on_display
import time
import logging
import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.INFO)

class MqttOLEDClient:
    def __init__(self, broker, port=1883, client_id=None, username=None, password=None):
        self.broker = broker
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password

        # Inicializa o cliente MQTT
        self.client = mqtt.Client(client_id)
        if username and password:
            self.client.username_pw_set(username, password)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        logging.info(f"Conectado ao broker MQTT com código: {rc}")
        client.subscribe("API/WAY")
        logging.info("Inscrito no tópico 'API/WAY'.")

    def on_message(self, client, userdata, msg):
        direction = msg.payload.decode().strip().lower()
        logging.info(f"Direção recebida: {direction}")
        disp, image, draw = init_display()
        dir = "frente"
        draw_triangle_on_display(disp, draw, image, dir)

    def connect_and_loop(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()
        logging.info("Aguardando mensagens... (Ctrl+C para sair)")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Desconectando...")
            self.client.loop_stop()
            self.client.disconnect()
            logging.info("Desconectado e display limpo.")

if __name__ == "__main__":
    mqtt_broker = "192.168.18.16"  # Ajuste para o IP do seu broker
    mqtt_port = 1883
    mqtt_client_id = "raspberry_pi_oled_client"
    #disp, image, draw = init_display()
    #dir = "frente"
    #draw_triangle_on_display(disp, draw, image, dir)
    #time.sleep(3)

    mqtt_oled_client = MqttOLEDClient(mqtt_broker, mqtt_port, mqtt_client_id)
    mqtt_oled_client.connect_and_loop()

