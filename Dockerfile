#build
FROM node:11.12.0-alpine as build-vue
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./client/package*.json ./
RUN npm install
COPY ./client .
RUN npm run build

#production
FROM nginx:stable-alpine as production
WORKDIR /app
RUN apk update && \
    apk add --no-cache \
    build-base \
    gcc musl-dev \
    libffi-dev \
    libressl-dev \
    openssl-dev \
    python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev libressl-dev libxml2 libxml2-dev libxslt libxslt-dev libjpeg-turbo-dev zlib-dev git
COPY --from=build-vue /app/dist /usr/share/nginx/html
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./server/requirements.txt ./
COPY ./server/Eurocode ./Eurocode
COPY ./server/utilities ./utilities
RUN apk update && pip install -r requirements.txt
#RUN pip install -e ./Eurocode
RUN pip install gunicorn
COPY ./server .
CMD gunicorn -b 0.0.0.0:5000 app:app --log-level=debug --daemon && \
    sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && \
    nginx -g 'daemon off;'