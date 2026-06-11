FROM python:3.12-slim

# Evita que o Python grave arquivos .pyc no disco
ENV PYTHONDONTWRITEBYTECODE=1
# Evita que o Python use buffer no stdout e stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta 8000 do Django
EXPOSE 8000

# Executa o entrypoint do Django
CMD ["python", "entrypoint.py"]
