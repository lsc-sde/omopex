FROM  mcr.microsoft.com/devcontainers/python:3.12

COPY requirements.txt /tmp/
RUN umask 0002 \
    && pip install -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt
