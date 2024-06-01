FROM python:3.10

RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://dl.min.io/server/minio/release/linux-amd64/minio -q \
    && chmod +x minio \
    && mv minio /usr/local/bin/

RUN mkdir /data

CMD ["minio", "server", "/data", "--access-log", "/dev/null", "--root-bucket", "images", "--default-expire", "300"]

WORKDIR /app
ENV $(cat .env-dev | xargs)
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "api.py"]
