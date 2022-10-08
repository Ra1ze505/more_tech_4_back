FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 10
ENV PYTHONDONTWRITEBYTECODE 10
ENV PYTHONPATH=/app
ENV MUSL_LOCPATH="/usr/share/i18n/locales/musl"


RUN apk add --no-cache \
    curl `# для установки poetry` \
    cargo `# rust manager` \
    gcc `# для установки poetry` \
    libffi-dev `# для установки poetry` \
    git `# для установки зависимостей из git` \
    build-base  `# для сборки пакетов`

COPY ./req.txt /code/req.txt

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir --upgrade -r /code/req.txt

RUN mkdir /app
WORKDIR /app/
COPY docker/wait-for /usr/bin/
RUN chmod +x /usr/bin/wait-for
COPY / /app/


