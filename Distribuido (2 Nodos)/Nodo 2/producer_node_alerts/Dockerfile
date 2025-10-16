FROM node:18-alpine
WORKDIR /app

COPY package.json ./
RUN npm install --production

COPY index.js .

ENV RABBIT_HOST=rabbitmq

CMD ["node", "index.js"]

