#!/bin/bash

API_URL="http://172.17.0.2:5000/detect-emotions"

for image_file in *.jpg; do
 if [ -f "$image_file" ]; then
  image_path=$(realpath "$image_file")
  encoded_data_file="/tmp/encoded_image.txt" # Temporary file for encoded data

  # Encode image and store in temporary file
  base64 -w 0 "$image_path" > "$encoded_data_file"

  # Read encoded data from temporary file
  image_data=$(cat "$encoded_data_file")

  # Properly format JSON payload with double quotes
  payload="{\"image_data\": \"$image_data\"}"
  CONTENT_TYPE="Content-Type: application/json"

  curl -X POST -H "$CONTENT_TYPE" -d "$payload" "$API_URL"

  # Clean up temporary file (optional)
  rm "$encoded_data_file"

  break
 fi
done
