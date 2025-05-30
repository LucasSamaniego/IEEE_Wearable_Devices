import networkx as nx
from pyzbar.pyzbar import decode
from picamera2 import Picamera2
import numpy as np
import cv2
import display
import logging
# Configura o logging para suprimir mensagens de info e debug
logging.getLogger('picamera2').setLevel(logging.WARNING)

# Função para determinar a direção com base nas coordenadas
def calcular_direcao(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    if abs(dx) > abs(dy):
        return "Direita" if dx > 0 else "Esquerda"
    else:
        return "Frente" if dy > 0 else "Trás"

# Função para ler e decodificar o QR Code usando Pyzbar
def ler_qr_code(frame):
    qr_codes = decode(frame)
    for qr_code in qr_codes:
        data = qr_code.data.decode('utf-8')
        return data
    return None

# Função para calcular a direção do próximo passo
def calcular_direcoes(nodos, G, pos_usuario, destino):
    shortest_path = nx.shortest_path(G, source=pos_usuario, target=destino, weight='weight')
    if len(shortest_path) < 2:
        return "Destino já alcançado ou caminho inválido"
    nodo_atual = shortest_path[0]
    nodo_proximo = shortest_path[1]
    direcao = calcular_direcao(nodos[nodo_atual], nodos[nodo_proximo])
    return direcao

#Função principal
def map(destino):
    try:    
        # Criando um grafo
        G = nx.Graph()

        # Adicionando nodos ao grafo com coordenadas (x, y)
        nodos = {
            "Entrada": (0, 0),
            "Corredor1": (5, 0),
            "Corredor2": (10, 0),
            "SalaA": (5, 5),
            "SalaB": (10, 5)
        }

        for nodo, pos in nodos.items():
            G.add_node(nodo, pos=pos)

        # Adicionando arestas manualmente conforme a primeira versão
        arestas = [
            ("Entrada", "Corredor1"),
            ("Corredor1", "Corredor2"),
            ("Corredor1", "SalaA"),
            ("Corredor2", "SalaB")
        ]

        for aresta in arestas:
            nodo1, nodo2 = aresta
            G.add_edge(nodo1, nodo2, weight=5)

        # Variável para rastrear a última posição do usuário
        ultima_posicao = None

        # Configurando a câmera com Picamera2
        picam2 = Picamera2()
        config = picam2.create_preview_configuration()
        picam2.configure(config)
        picam2.start()

        print("Lendo QR Code...")
        pos_usuario = None

        while not(pos_usuario in G.nodes):
            # Capturando o frame da câmera
            frame = picam2.capture_array()
                
            # Convertendo a imagem para o formato correto
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Lendo o QR Code
            pos_usuario = ler_qr_code(frame_rgb)
        
        picam2.close()

        if pos_usuario != destino:
            print(pos_usuario)
            if pos_usuario in G.nodes:
                print(f"\nPosição atual do usuário: {pos_usuario}")
                            
                # Calculando a próxima direção a ser seguida
                proxima_direcao = calcular_direcoes(nodos, G, pos_usuario, destino)
                display.show(proxima_direcao) #FUNÇÃO PARA MOSTRAR A SETA DE DIREÇÃO NO DISPLAY
                            
                return pos_usuario
        else:
            return pos_usuario
    finally:
        picam2.close()
    
def off():
    picam2 = Picamera2()
    picam2.close()