#build
FROM node:11.12.0-alpine as build-vue
WORKDIR /app
#ENV PATH /app/node_modules/.bin:$PATH
COPY ./client/package*.json ./
RUN npm install
COPY ./client .
RUN npm run build

#production
FROM nginx:stable-alpine as production
COPY --from=build-vue /app/dist /usr/share/nginx/html
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 800
CMD ["nginx", "-g", "daemon off;"]