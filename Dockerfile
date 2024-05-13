FROM alpine

ARG branch=main
ENV GIT_REPO_URL=https://github.com/milinsoft/bank_app
ENV PROJECT_FOLDER=/app/bank_app

WORKDIR /app

RUN set -ex \
    && apk add --update --no-cache git python3 py3-pip \
    && git clone $GIT_REPO_URL $PROJECT_FOLDER -b $branch --depth=1 \
    && python3 -m venv venv \
    && source venv/bin/activate \
    && pip install -r $PROJECT_FOLDER/requirements.txt \
    && apk del git \
    && rm -rf /var/cache/apk/* /root/.cache $PROJECT_FOLDER/.git

ENTRYPOINT ["sh"]
CMD ["-c", "/app/venv/bin/python bank_app"]
