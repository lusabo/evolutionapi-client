# Usar uma imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos necessários para o container
COPY app.py /app/

# Instalar as dependências necessárias
RUN pip install flask uv

# Expor a porta 3000 para acessar a aplicação
EXPOSE 3000