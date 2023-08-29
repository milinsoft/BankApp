FROM alpine

WORKDIR /app

RUN apk add --update --no-cache git python3 py3-pip \
    && git clone https://github.com/milinsoft/bank_app /app/bank_app \
    && pip install -r /app/bank_app/requirements.txt \
    && ln -sf /usr/bin/python3.11 /usr/bin/python \
    && rm -rf /var/lib/apt/lists/

CMD ["python3", "bank_app"]
