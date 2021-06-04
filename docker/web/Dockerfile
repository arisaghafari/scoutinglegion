# pull official base image
FROM python:3.8.3-alpine

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
    python3-dev \
    libxslt-dev


RUN apk add libffi-dev openssl-dev

RUN apk add rust \
            cargo
RUN apk add cairo-dev \
            libxmu-dev \
            pango-dev \
            perl \
            tk-dev


RUN pip install --upgrade pip
RUN /usr/local/bin/python -m pip install --upgrade pip
# RUN apk add postgresql-contrib
RUN pip install cryptography
RUN apk add postgresql-dev

RUN pip install psycopg2

RUN apk add --no-cache jpeg-dev zlib-dev

RUN echo "http://mirror.leaseweb.com/alpine/edge/community" >> /etc/apk/repositories
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk add --virtual .build-deps \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/community \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        gcc libc-dev geos-dev geos && \
    runDeps="$(scanelf --needed --nobanner --recursive /usr/local \
    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
    | xargs -r apk info --installed \
    | sort -u)" && \
    apk add --virtual .rundeps $runDeps
RUN ["pip", "install", "shapely"]

RUN mkdir scoutinglegion

COPY requirements.txt /scoutinglegion
RUN pip install -r /scoutinglegion/requirements.txt
COPY . /scoutinglegion

RUN rm /scoutinglegion/index.html


RUN rm /usr/local/lib/python3.8/site-packages/rest_framework_swagger/templates/rest_framework_swagger/index.html
COPY index.html /usr/local/lib/python3.8/site-packages/rest_framework_swagger/templates/rest_framework_swagger/

WORKDIR /scoutinglegion
EXPOSE 8000

#CMD ["gunicorn", "ScoutingLegion.wsgi", ":8000"]