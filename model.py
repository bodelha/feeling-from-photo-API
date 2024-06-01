from transformers import pipeline
from PIL import Image
from urllib.request import urlopen


def detect_emotions(image_url):
  """
  Detects emotions from an image provided by URL.

  Args:
      image_url: The URL of the image to process.

  Returns:
      The predicted emotion label (e.g., "Felicidade", "Raiva") or None if processing fails.
  """

  try:
    # Download the image from the URL
    response = urlopen(image_url)
    image_data = response.read()

    # Convert data to PIL Image
    image = Image.open(io.BytesIO(image_data))

    # Process image
    pipe = pipeline("image-classification", model="dima806/facial_emotions_image_detection")
    results = pipe(image)
    predicted_class = results[0]["label"]

    # Map predicted class to emotion name (optional)
    emotion_names = {
      "happy": "Felicidade",
      "angry": "Raiva",
      "sad": "Tristeza",
      "neutral": "Neutro",
      "surprised": "Surpresa",
      "fearful": "Medo",
    }
    return emotion_names.get(predicted_class)

  except Exception as e:
    print(f"Error processing image: {e}")
    return None
