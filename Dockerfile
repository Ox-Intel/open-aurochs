# syntax=docker/dockerfile:1.7
#
# Unified Dockerfile with multi-stage targets.
#   docker compose build           → target: dev
#   suzuri deploy / docker build … → --target=runtime
#
# Production JS bundle is built in the `js_build` side stage (Node 22 +
# FontAwesome NPM token, declared via `build_args:` in suzuri.yaml). Local
# dev uses `yarn watch` on the host; compiled JS lives in the bind-mounted
# source tree, so the dev image doesn't need Node.

# ============== js_build ==============
# Side stage — only `builder` pulls from it via COPY --from. Dev never builds
# this stage (Docker skips stages not on the path to the requested target).
FROM node:22-slim AS js_build

ARG FONTAWESOME_NPM_TOKEN
ENV FONTAWESOME_NPM_TOKEN=${FONTAWESOME_NPM_TOKEN}

ADD aurochs /project/aurochs
ADD bin /project/bin

WORKDIR /project
RUN ./bin/build_js_apps.sh \
    && rm -rf \
        aurochs/apps/webapp/.yarn aurochs/apps/webapp/node_modules \
        aurochs/apps/public/.yarn aurochs/apps/public/node_modules \
        node_modules


# ============== base ==============
# WeasyPrint dlopens pango/gobject via CFFI at module load time, so its
# runtime libs need to be present in any stage that imports the Django apps
# (including `collectstatic` in builder and `runserver` in dev).
FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/opt/venv/bin:$PATH" \
    TZ=UTC \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential libpq-dev libmagic-dev \
        libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 \
        tesseract-ocr poppler-utils libarchive-dev \
        tzdata curl ca-certificates \
    && ln -fs /usr/share/zoneinfo/UTC /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && python -m venv /opt/venv \
    && groupadd -r appuser \
    && useradd -r -g appuser -d /home/appuser -m appuser \
    && mkdir -p /app \
    && chown -R appuser:appuser /opt/venv /app

USER appuser
WORKDIR /app

COPY --chown=appuser:appuser requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# ============== dev ==============
FROM base AS dev

CMD ["uvicorn", "aurochs.asgi:application", \
     "--host", "0.0.0.0", "--port", "8000", "--reload"]


# ============== builder ==============
FROM base AS builder

USER appuser
WORKDIR /app

# Bring in the JS-built Django module and helper scripts.
COPY --from=js_build --chown=appuser:appuser /project/aurochs ./aurochs
COPY --from=js_build --chown=appuser:appuser /project/bin ./bin
COPY --chown=appuser:appuser manage.py ./

RUN DJANGO_SETTINGS_MODULE=aurochs.envs.production \
    DJANGO_SECRET_KEY=build-placeholder \
    AUROCHS_FRIENDLY_NAME=build \
    AUROCHS_NAMESPACE=build \
    AUROCHS_ENCRYPTION_KEY=build-placeholder-key \
    AUROCHS_ENCRYPTION_SALT=build-placeholder-salt \
    AUROCHS_DOMAIN=localhost \
    AUROCHS_ADMIN_NAME=build \
    AUROCHS_ADMIN_EMAIL=build@localhost \
    AUROCHS_FROM_EMAIL=build@localhost \
    DATABASE_URL=sqlite:///tmp/build.db \
    python manage.py collectstatic --noinput

# Strip source maps and test artifacts from the built static output.
RUN rm -rf \
        collected_static/client/static/js/*.map \
        collected_static/client/static/js/*.map.br \
        collected_static/client/static/js/*.map.gz \
        collected_static/client/js/*.map \
        collected_static/client/js/*.map.br \
        collected_static/client/js/*.map.gz \
        cypress postman tests


# ============== runtime ==============
FROM python:3.12-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    TZ=UTC \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata curl \
        libpq5 libmagic1 \
        libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 \
        tesseract-ocr poppler-utils \
    && ln -fs /usr/share/zoneinfo/UTC /etc/localtime \
    && dpkg-reconfigure --frontend noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r appuser \
    && useradd -r -g appuser -d /home/appuser -m appuser

USER appuser
WORKDIR /app

COPY --from=builder --chown=appuser:appuser /opt/venv /opt/venv
COPY --from=builder --chown=appuser:appuser /app /app

EXPOSE 8000

CMD ["uvicorn", "aurochs.asgi:application", \
     "--host", "0.0.0.0", "--port", "8000", \
     "--workers", "4"]
