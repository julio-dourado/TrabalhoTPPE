# Multi-stage build para melhor performance e cache
FROM python:3.11-slim as base

# Configurações básicas
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

# Instalar dependências do sistema (layer que raramente muda)
RUN apt-get update && apt-get install -y \
  postgresql-client \
  curl \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get clean

# Stage para dependências Python (otimizado para cache)
FROM base as deps
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

# Stage de desenvolvimento (com volumes para hot reload)
FROM deps as development
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Stage de produção (otimizado)
FROM deps as production
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 