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
ADD requirements.txt ./
RUN apk update && pip install -r requirements.txt
ADD . .
RUN pip install gunicorn