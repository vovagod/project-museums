# Образец
ARG DOCKER_REGISTRY
FROM $DOCKER_REGISTRY/python-39:latest

ARG REQUIREMENTS_PREFIX
ARG INDEX_URL
ARG TRUSTED_HOST
ARG EXTRA_INDEX_URL

ENV PIP_INDEX_URL=$INDEX_URL
ENV PIP_TRUSTED_HOST=$TRUSTED_HOST
ENV PIP_EXTRA_INDEX_URL=$EXTRA_INDEX_URL

USER root

RUN rm -rf /usr/lib/node_modules/npm/node_modules/cross-spawn/ \
           /usr/lib/python3.6/site-packages/idna-2.5-py3.6.egg-info
COPY ubi.repo /etc/yum.repos.d/ubi.repo

COPY *.crt /etc/pki/ca-trust/source/ancors/
RUN update-ca-trust extract

ENV REQUESTS_CA_BUNDLE="/etc/ssl/certs/ca-bundle.crt"

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /quota
ENV SRC_PATH=/quota/src
COPY . .

RUN pip3 install --upgrade pip && pip3 install -r ${REQUIREMENTS_PREFIX}requirements.txt

RUN cat /etc/pki/ca-trust/source/anchors/SberBankRootCA.crt >> /opt/app-root/lib64/python3.9/site-packages/certifi/cacert.pem

ENV DJANGO_SETTINGS_MODULE django_app.DJANGO_SETTINGS_MODULE

RUN set -ex\
    yum install -y --no-install-recommends tzdata && \
    rm -rf /etc/localtime /etc/packages && \
    ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime

RUN chgrp -R 0 /quota && chmod -R g=u /quota

EXPOSE 8080

USER 1001
ENTRYPOINT ['/quota/docker-entrypoint.sh']
