FROM tiangolo/meinheld-gunicorn:python3.7-alpine3.8

WORKDIR app

RUN mkdir LinkShower

COPY LICENSE README.md linkshower.py requirements.txt templates static ./LinkShower

WORKDIR app/LinkShower

RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/cache/apk/* && \
    apk del git ca-certificates

ENV MODULE_NAME="LinkShower.linkshower"
