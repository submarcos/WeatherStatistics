FROM ubuntu:jammy as base

ENV PYTHONBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8
ENV TZ UTC
ENV POSTGRES_HOST db
ENV POSTGRES_PORT 5432

RUN apt-get -y -qq update \
    && apt-get -y -qq install \
    python3 \
    libpq5 \
    postgresql-client \
    tzdata \
    netcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives/*

RUN adduser django
RUN mkdir -p /opt/weather && chown django:django /opt
WORKDIR /opt/weather

COPY .docker/backend/entrypoint.sh /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
EXPOSE 8000

FROM base as build

RUN apt-get -y -qq update \
    && apt-get -y -qq install \
    python3-dev \
    python3-venv \
    build-essential \
    libpq-dev \
    gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives/*

USER django

RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir --upgrade pip wheel

COPY requirements.txt /opt/weather/requirements.txt
RUN /opt/venv/bin/pip install --no-cache-dir --upgrade -r /opt/weather/requirements.txt

FROM build as dev

COPY dev-requirements.txt /opt/weather/dev-requirements.txt
RUN /opt/venv/bin/pip install --no-cache-dir --upgrade -r /opt/weather/dev-requirements.txt

CMD /opt/venv/bin/python manage.py runserver 0.0.0.0:8000

FROM base as prod

COPY manage.py /opt/weather/manage.py
COPY --from=build /opt/venv /opt/venv
COPY project /opt/weather/project

RUN ["./manage.py", "compilemessages"]

USER root

RUN apt-get -y -qq update \
    && apt-get -y -qq full-upgrade \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives/*

USER django

CMD /opt/venv/bin/gunicorn backend.wsgi:application 0.0.0.0:8000