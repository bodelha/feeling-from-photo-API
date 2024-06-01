#!/bin/bash

API_URL="http://172.17.0.2:5000/detect-emotions"

for image_file in *.jpg; do
    if [ -f "$image_file" ]; then
        image_path=$(realpath "$image_file")
        encoded_data=$(base64 -w 0 "$image_path")
        payload="{\"image_data\": \"$encoded_data\"}"
        CONTENT_TYPE="Content-Type: application/json"

        curl -X POST -H "$CONTENT_TYPE" -d "$payload" "$API_URL"

        # Clean up temporary file (optional)
        # rm "$encoded_data_file"

        break
    fi
done
