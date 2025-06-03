# Imagem base (Python 3.11 como exemplo)
FROM python:3.11-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos para o container
COPY . .

# Comando para rodar seu script Python
CMD ["python", "main.py"]
