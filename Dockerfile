FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pandas pymongo polars

COPY ./scripts/import_script.py /scripts/import_script.py
COPY ./scripts/polar_request.py /scripts/polar_request.py

CMD ["tail", "-f", "/dev/null"]
