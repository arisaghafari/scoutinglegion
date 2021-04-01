# pull official base image
FROM python:3.8.3-alpine

# set work directory
#WORKDIR /usr/src/app
WORKDIR /scoutinglegion

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk update && apk upgrade
RUN apk add gcc \
    g++ \
    linux-headers \
    musl-dev \
    make \
    libxml2-dev \
    libressl-dev \
    python3-dev


RUN apk add libffi-dev openssl-dev

RUN apk add rust \
            cargo
RUN apk add cairo-dev \
            libxmu-dev \
            pango-dev \
            perl \
            tk-dev


RUN pip install --upgrade pip

RUN pip install cryptography
RUN apk add postgresql-dev

RUN pip install psycopg2

RUN apk add --no-cache jpeg-dev zlib-dev
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# run entrypoint.sh
#ENTRYPOINT ["/scoutinglegion/entrypoint.sh"]