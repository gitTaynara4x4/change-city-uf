# Passo 1: Escolha uma imagem base com Python
FROM python:3.9-slim

# Passo 2: Defina o diretório de trabalho no container
WORKDIR /app

# Passo 3: Copie o código Python (script.py) para o container
COPY . /app

# Passo 4: Instale as dependências (requests)
RUN pip install --no-cache-dir requests

# Passo 5: Defina o comando para rodar o script Python
CMD ["python", "script.py"]
