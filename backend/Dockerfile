FROM python:3.10

# Instale dependências de sistema para psycopg2
RUN apt-get update && \
  apt-get install -y libpq-dev gcc && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .