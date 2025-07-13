FROM tiangolo/meinheld-gunicorn:python3.9

RUN mkdir /app/LinkShower
RUN mkdir -p /app/LinkShower/static/styles
RUN mkdir /app/LinkShower/templates

COPY LICENSE README.md linkshower.py requirements.txt /app/LinkShower/
COPY templates/links.html templates/top.html /app/LinkShower/templates/
COPY static/styles/main.css /app/LinkShower/static/styles/

WORKDIR /app/LinkShower

RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/cache/apk/*

ENV MODULE_NAME="LinkShower.linkshower"
