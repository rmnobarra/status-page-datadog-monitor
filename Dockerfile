# Usa uma imagem oficial do Python slim
FROM python:3.12-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências
COPY requirements.txt ./

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt \
    gunicorn uvicorn

# Copia o restante do código para o container
COPY . .

# Expõe a porta da aplicação
EXPOSE 8000

# Comando de entrada (produção)
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000"]
