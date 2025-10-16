FROM node:18-alpine

WORKDIR /app

# Copia solo package.json
COPY package.json ./

# Instala dependencias sin usar package-lock.json
RUN npm install --production

# Copia el código fuente
COPY index.js .

# Variable de entorno para conectar al broker
ENV RABBIT_HOST=rabbitmq

# Ejecuta el productor
CMD ["node", "index.js"]

