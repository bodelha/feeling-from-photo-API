import base64
import json
from flask import Flask, request, jsonify
from model import detect_emotions
from minio import Minio
from minio.error import S3Error
from uuid import uuid4
import io

MINIO_URL = "127.0.0.1:9000"
MINIO_BUCKET = "images"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"

app = Flask(__name__)

# Initialize MinIO client
client = Minio(
    MINIO_URL,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# Ensure bucket exists
if not client.bucket_exists(MINIO_BUCKET):
    client.make_bucket(MINIO_BUCKET)

@app.route("/detect-emotions", methods=["POST"])
def detect_emotions_endpoint():
    try:
        data = request.get_json()
        image_data_base64 = data["image_data"]

        # Decode base64 data
        image_data_bytes = base64.b64decode(image_data_base64)

        # Generate unique filename
        filename = f"{uuid4()}.jpg"

        # Upload image to Minio bucket
        image_data_stream = io.BytesIO(image_data_bytes)
        client.put_object(
            MINIO_BUCKET, 
            filename, 
            image_data_stream, 
            length=len(image_data_bytes), 
            content_type="image/jpeg"
        )

        # Generate image URL
        image_url = f"http://{MINIO_URL}/{MINIO_BUCKET}/{filename}"

        # Call emotion detection with image URL
        emotions = detect_emotions(image_url)
        print(emotions)

        return jsonify({"emotions": emotions})

    except S3Error as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
