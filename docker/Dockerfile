FROM python:3.10-alpine

ARG POETRY_PARAMS=""
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="${PATH}:/root/.local/bin"

EXPOSE 2007

WORKDIR /code

COPY ../req.txt /code/req.txt

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir --upgrade -r /code/req.txt

COPY ../src /code/src


