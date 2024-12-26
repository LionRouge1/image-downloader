import requests
from io import BytesIO
from PIL import Image
import re

image_url = "https://sdbooth2-production.s3.amazonaws.com/hm664gvuunhkdnowt0i81lt0bp6o"
response = requests.get(image_url)
response.raise_for_status()
content_disposition = response.headers.get('Content-Disposition')
if content_disposition:
  filename = re.findall('filename="(.+)"', content_disposition)
  if filename:
    image_name = filename[0]
  else:
    image_name = "unknown"
else:
  # Fallback to extracting the filename from the URL
  image_name = image_url.split("/")[-1]
image_data = BytesIO(response.content)
img = Image.open(image_data)
print(filename, type(img.format), img.size)