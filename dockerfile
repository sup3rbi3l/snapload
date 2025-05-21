# Imagem base com Python 3.12
FROM python:3.12-slim

# Instala ffmpeg e dependências básicas
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instala as dependências do seu projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do seu código
COPY . /app
WORKDIR /app

# Comando para rodar sua aplicação
CMD ["python", "app.py"]
