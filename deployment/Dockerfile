FROM python:3.9
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/flatype
COPY src /opt/flatype/src
COPY deployment/.env /opt/flatype/deployment/

RUN pip install -U pip && pip install -r src/requirements.txt
