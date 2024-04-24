FROM alpine

ENV GIT_REPO_URL=https://github.com/milinsoft/bank_app
ENV PROJECT_FOLDER=/app/bank_app

WORKDIR /app

RUN set -ex \
    && apk add --update --no-cache git python3 python3-dev py3-pip \
    && git clone $GIT_REPO_URL $PROJECT_FOLDER -b main --depth=1\
    && python3 -m venv venv \
    && chmod +x ./venv/bin/activate \
    && . ./venv/bin/activate \
    && pip install -r $PROJECT_FOLDER/requirements.txt\
    && apk del git \
    && rm -rf /var/cache/apk/* /root/.cache $PROJECT_FOLDER/.git

# TODO: Add PostgreSQL, add Docker build based on a current branch
CMD ["/app/venv/bin/python3.11", "bank_app"]
