FROM python:3.10

RUN apt-get update && \
  apt-get install -y libpq-dev gcc curl && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y build-essential

COPY . .