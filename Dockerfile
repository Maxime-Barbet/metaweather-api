FROM python:3-slim
LABEL maintainer="maxibarbet@gmail.com"

RUN mkdir /app \
    && addgroup --gid 2001 peopledoc \
    && adduser --uid 1001 --disabled-password --gecos "" peopledoc --ingroup peopledoc

COPY . /app

RUN chown -R peopledoc:peopledoc /app \
    && /app/install.sh

USER peopledoc

ENTRYPOINT ["/app/run.sh"]