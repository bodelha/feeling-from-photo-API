#!/bin/bash

# Inicie o MinIO em segundo plano
minio server /data --console-address ":9001" &

# Espere o MinIO iniciar
sleep 5

# Inicie a aplicação Flask
python api.py
