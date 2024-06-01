import base64
import json
from flask import Flask, request, jsonify
from model import detect_emotions
from minio import Minio
from uuid import uuid4

MINIO_URL = "http://minio-server:9000"
MINIO_BUCKET = "images"

app = Flask(__name__)


@app.route("/detect-emotions", methods=["POST"])
def detect_emotions_endpoint():
    try:
        data = request.get_json()
        print(data)
        image_data_base64 = data["image_data"]

        # Decode base64 data
        image_data_bytes = base64.b64decode(image_data_base64)

        # Generate unique filename
        filename = f"{uuid4()}.jpg"

        # Upload image to Minio bucket
        client = Minio(
            MINIO_URL,
        )
        client.put_object(MINIO_BUCKET, filename, image_data_bytes, content_type="image/jpeg")

        # Generate image URL
        image_url = f"{MINIO_URL}/{MINIO_BUCKET}/{filename}"

        # Call emotion detection with image URL
        emotions = detect_emotions(image_url)
        print(emotions)

        return jsonify({"emotions": emotions})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
