FROM python:3.6-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk update \
    && apk add --no-cache gcc linux-headers make python3-dev musl-dev g++ \
    && apk add --no-cache mariadb-dev

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 30030

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]
