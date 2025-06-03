# Usar uma imagem base Python leve
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos de requisitos (se houver) para instalar dependências
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código da aplicação para dentro do container
COPY . .

# Expor a porta que o Flask vai usar
EXPOSE 8000

# Comando para rodar a aplicação Flask
CMD ["python", "main.py"]
