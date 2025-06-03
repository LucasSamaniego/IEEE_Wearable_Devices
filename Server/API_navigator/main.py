# Instale o FastAPI e o uvicorn antes, se ainda não tiver:
# pip install fastapi uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import heapq

app = FastAPI()

# Definição do grafo (usando dicionário de adjacência)
grafo = {
    "P1": {"M7": 2, "G3": 1, "P3": 4},
    "M7": {"P1": 2, "M2": 3},
    "G3": {"P1": 1},
    "M2": {"M7": 3, "P3": 1},
    "P3": {"P1": 4, "M2": 1}
}

# Mapeamento de direções entre pares de nós
direcoes = {
    ("P1", "M7"): "frente",
    ("P1", "G3"): "direita",
    ("P1", "P3"): "trás",
    ("M7", "P1"): "trás",
    ("M7", "M2"): "direita",
    ("M2", "M7"): "esquerda",
    ("M2", "P3"): "frente",
    ("P3", "M2"): "trás",
    ("P3", "P1"): "frente",
    ("G3", "P1"): "esquerda"
}

# Função de Dijkstra para encontrar o menor caminho
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

    # Calcula o caminho mais curto
    caminho = dijkstra(atual, objetivo)

    if not caminho or len(caminho) < 2:
        return JSONResponse(content={"erro": "Caminho não encontrado"}, status_code=404)

    # Primeira direção a seguir
    proximo_no = caminho[1]
    direcao = direcoes.get((atual, proximo_no), "direção desconhecida")

    return JSONResponse(content={
        "caminho": caminho,
        "primeira_direcao": direcao
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)

# Para rodar o servidor:
# uvicorn nome_do_arquivo:app --reload
