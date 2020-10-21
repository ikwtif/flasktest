FROM node:11.12.0-alpine as build-vue
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
ADD ./package*.json ./
RUN npm install
ADD . .
RUN npm run build