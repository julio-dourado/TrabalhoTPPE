# Usar a imagem oficial do Node.js
FROM node:18-alpine

# Instalar curl para healthcheck
RUN apk add --no-cache curl

# Definir o diretório de trabalho
WORKDIR /app

# Copiar package.json e package-lock.json
COPY package*.json ./

# Instalar dependências
RUN npm install

# Copiar o resto do código da aplicação
COPY . .

# Expor a porta que a aplicação irá rodar
EXPOSE 3000

# Comando para iniciar o servidor de desenvolvimento
CMD ["npm", "run", "dev"] 