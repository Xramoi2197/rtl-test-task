FROM mongo:latest
WORKDIR /usr/src/app
COPY ./dump /usr/src/app/dump
EXPOSE 27017

COPY ./sampleDB.js /docker-entrypoint-initdb.d/
