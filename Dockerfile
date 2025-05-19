# Usa imagem leve com Python
FROM python:3.12.2

# Instala ffmpeg e dependências
RUN apt-get update && apt-get install -y ffmpeg curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta padrão Flask
EXPOSE 5000

# Comando para rodar o servidor
CMD ["python", "app.py"]
