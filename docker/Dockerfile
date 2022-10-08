FROM python:3.10

ENV PYTHONUNBUFFERED 10
ENV PYTHONDONTWRITEBYTECODE 10
ENV PYTHONPATH=/app
ENV MUSL_LOCPATH="/usr/share/i18n/locales/musl"
ENV GET_POETRY_IGNORE_DEPRECATION=1

RUN apt-get -y update
RUN apt-get -y upgrade

COPY ./req.txt /code/req.txt

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN mkdir /app
COPY pyproject.toml poetry.lock /app/
WORKDIR /app/

RUN poetry install

COPY docker/entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh
COPY / /app/


