FROM python:3.10

RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://dl.min.io/server/minio/release/linux-amd64/minio -q \
    && chmod +x minio \
    && mv minio /usr/local/bin/

RUN mkdir /data

ENV $(cat .env | xargs)

WORKDIR /app
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
COPY . .
RUN pip install -r requirements.txt

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
