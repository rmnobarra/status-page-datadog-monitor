# Imagem base
FROM python:3.12-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos necessários
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponha a porta
EXPOSE 8000

# Executa a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
