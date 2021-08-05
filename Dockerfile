FROM python:3.9
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/projects/flatype
COPY . /usr/projects/flatype/
RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt
