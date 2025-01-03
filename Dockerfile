# Base image com Python 3.12
FROM python:3.12

# Diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar arquivos necessários para o contêiner
COPY app ./app
COPY run.py ./

# Instalar as dependências diretamente
RUN pip install --no-cache-dir \
    flask>=3.1.0 \
    openai>=1.58.1 \
    python-dotenv>=1.0.1 \
    requests>=2.32.3 \
    whisper>=1.1.10 \
    pycryptodome>=3.11.0 \
    uv

# Expôr a porta do Flask
EXPOSE 3000