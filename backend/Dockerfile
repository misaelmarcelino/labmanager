# ================================
# Dockerfile - Backend FastAPI
# ================================
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Evita buffering de logs
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Instala dependências de sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia dependências e instala
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o código da aplicação
COPY . .

# Exposição da porta
EXPOSE 8000

# Comando padrão (Uvicorn com reload desativado)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
