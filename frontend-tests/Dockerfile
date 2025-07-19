FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
  wget \
  curl \
  unzip \
  gnupg \
  && rm -rf /var/lib/apt/lists/*

# Instalar Chrome versão estável específica
RUN wget -q -O /tmp/chrome.deb "https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.90-1_amd64.deb" \
  && apt-get update \
  && apt-get install -y /tmp/chrome.deb \
  && rm /tmp/chrome.deb \
  || (echo "Fallback to latest Chrome" \
  && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update \
  && apt-get install -y google-chrome-stable)

# Configurar diretório de trabalho
WORKDIR /tests

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de teste
COPY . .

# Comando padrão
CMD ["python", "-m", "pytest", "-v", "--html=reports/report.html", "--self-contained-html"] 