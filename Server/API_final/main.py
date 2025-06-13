from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import heapq

app = FastAPI()

setores = ["Apoio", "C-95", "C-97", "C-98", "IU-93", "SSS", "T-25", "T-27"]
prateleiras = [1, 2, 3]
colunas = list(range(1, 22))  # colunas 1 a 21

def no(setor, prateleira, coluna):
    return f"{setor}-{prateleira}-{coluna}"

grafo = {}
direcoes = {}

# Construção do grafo: conexões internas
for setor in setores:
    for pr in prateleiras:
        for col in colunas:
            atual = no(setor, pr, col)
            grafo[atual] = {}

            # Horizontal: esquerda e direita na mesma prateleira
            if col > 1:
                esquerda = no(setor, pr, col - 1)
                grafo[atual][esquerda] = 1
                direcoes[(atual, esquerda)] = "esquerda"
            if col < 21:
                direita = no(setor, pr, col + 1)
                grafo[atual][direita] = 1
                direcoes[(atual, direita)] = "direita"

            # Vertical: subir e descer na mesma coluna
            if pr > 1:
                abaixo = no(setor, pr - 1, col)
                grafo[atual][abaixo] = 1
                direcoes[(atual, abaixo)] = "descer"
            if pr < 3:
                acima = no(setor, pr + 1, col)
                grafo[atual][acima] = 1
                direcoes[(atual, acima)] = "subir"

# Conexões entre setores adjacentes nas entradas e saídas (mesma prateleira)
for i in range(len(setores) - 1):
    atual_setor = setores[i]
    prox_setor = setores[i + 1]

    for pr in prateleiras:
        # Entrada (coluna 1)
        atual_entrada = no(atual_setor, pr, 1)
        prox_entrada = no(prox_setor, pr, 1)
        grafo[atual_entrada][prox_entrada] = 1
        grafo[prox_entrada][atual_entrada] = 1
        direcoes[(atual_entrada, prox_entrada)] = "frente"
        direcoes[(prox_entrada, atual_entrada)] = "trás"

        # Saída (coluna 21)
        atual_saida = no(atual_setor, pr, 21)
        prox_saida = no(prox_setor, pr, 21)
        grafo[atual_saida][prox_saida] = 1
        grafo[prox_saida][atual_saida] = 1
        direcoes[(atual_saida, prox_saida)] = "frente"
        direcoes[(prox_saida, atual_saida)] = "trás"

# Função de Dijkstra para encontrar menor caminho
def dijkstra(origem, destino):
    fila = [(0, origem, [])]
    visitados = set()

    while fila:
        (custo, no_atual, caminho) = heapq.heappop(fila)
        if no_atual in visitados:
            continue

        caminho = caminho + [no_atual]
        visitados.add(no_atual)

        if no_atual == destino:
            return caminho

        for vizinho, peso in grafo.get(no_atual, {}).items():
            if vizinho not in visitados:
                heapq.heappush(fila, (custo + peso, vizinho, caminho))

    return None

@app.post("/processar/")
async def processar(request: Request):
    dados = await request.json()
    atual = dados.get("atual")
    objetivo = dados.get("objetivo")

    if not atual or not objetivo:
        return JSONResponse(content={"erro": "Parâmetros 'atual' e 'objetivo' são obrigatórios"}, status_code=400)

    caminho = dijkstra(atual, objetivo)

    if not caminho or len(caminho) < 2:
        return JSONResponse(content={"erro": "Caminho não encontrado"}, status_code=404)

    proximo_no = caminho[1]
    direcao = direcoes.get((atual, proximo_no), "direção desconhecida")

    return JSONResponse(content={
        "caminho": caminho,
        "primeira_direcao": direcao
    })

# Para rodar o servidor: uvicorn nome_do_arquivo:app --reload
