FROM node:18-alpine

WORKDIR /app

# Copia solo package.json
COPY package.json ./

# Instala dependencias
RUN npm install --production

# Copia el código fuente
COPY index.js .

# Variable de entorno para el host del broker
ENV RABBIT_HOST=rabbitmq

# Ejecuta el consumidor
CMD ["node", "index.js"]

