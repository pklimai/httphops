FROM alpine:3.10

RUN apk add --no-cache build-base python3-dev \
    && pip3 install requests \
    && apk del -r --purge gcc make g++ \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && rm -rf /var/cache/apk/*

EXPOSE 8000

COPY docker-entrypoint.sh /
COPY httphops.py /

ENTRYPOINT ["/docker-entrypoint.sh"]
