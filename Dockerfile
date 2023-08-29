FROM alpine

ENV GIT_REPO_URL=https://github.com/milinsoft/bank_app
ENV PROJECT_FOLDER=/app/bank_app

WORKDIR /app

RUN set -ex \
    && apk add --update --no-cache git python3 py3-pip \
    && git clone $GIT_REPO_URL $PROJECT_FOLDER \
    && pip install -r $PROJECT_FOLDER/requirements.txt \
    && ln -sf /usr/bin/python3.11 /usr/bin/python \
    && apk del git \
    && rm -rf /var/cache/apk/* /root/.cache $PROJECT_FOLDER/.git

CMD ["python3", "bank_app"]
