# In dev, we build JS locally with `yarn watch`
# For production, build locally with `yarn build` before deploying
# FROM node:18.12-slim AS js_build
# ADD aurochs /app/aurochs
# ADD bin /app/bin
# WORKDIR /app
# RUN ./bin/build_js_apps.sh

FROM python:3.12.7-slim
MAINTAINER Steven Skoczen <steven@oxintel.ai>

# Add files
ADD bin /app/bin

WORKDIR /app

# COPY --from=js_build /app/aurochs ./aurochs


# Install the image os dependencies
RUN /app/bin/docker-install.sh

RUN export DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    tzdata \
    curl \
    npm \
    libpq-dev \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \ 
    links \
    elinks \
    tesseract-ocr \
    poppler-utils \
    libarchive-dev


# Handle tzdata in non-interative mode.
RUN ln -fs /usr/share/zoneinfo/UTC /etc/localtime; dpkg-reconfigure --frontend noninteractive tzdata

# Set up reqs
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Add procfile (for honcho)
ADD Procfile.dev /app/Procfile.dev
ADD manage.py /app/manage.py

# Explicitly add the env
ADD .env /app/.env

# Build apps and collect static
# RUN export $(grep -v '^#' /project/.env | xargs -d '\n') && /project/bin/build_and_cleanup.sh

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8