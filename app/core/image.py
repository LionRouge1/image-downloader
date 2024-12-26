import requests
from io import BytesIO
from PIL import Image
from decimal import Decimal
import re

class ImageDataError(Exception):
  pass

class ImageData:
  def __init__(self, url):
    self.url = url
    try:
      self.response = requests.get(url)
      self.response.raise_for_status
    except requests.RequestException as e:
      raise ImageDataError(f"Failed to fetch image from URL: {e}")
    
    self.image_data = BytesIO(self.response.content)
    self.image = Image.open(self.image_data)

  def image_name(self):
    image_name = 'default_name'
    content_disposition = self.response.headers.get('Content-Disposition')
    if content_disposition:
      filename = re.findall('filename="(.+)"', content_disposition)
      if filename:
        image_name = filename[0]
    return image_name
  
  def get_file_size(self):
    number = Decimal(len(self.response.content) / (1024 * 1024))
    formatted_number = number.quantize(Decimal("0.001"))
    return formatted_number
  
  def image_properties(self):
    return {
      "format": self.image.format,
      "size": self.image.size,
      "filename": self.image_name(),
      "mode": self.image.mode,
      "file_size": self.get_file_size(),
      "info": self.image.info
    }
  
  def display_image(self):
    try:
      img = self.image.resize((200, 200), Image.NEAREST)  # Use Image.LANCZOS instead of Image.ANTIALIAS
      img_byte_arr = BytesIO()
      format = self.image_properties()['format']
      img.save(img_byte_arr, format=format)
      img_byte_arr = img_byte_arr.getvalue()

      return img_byte_arr
    except Exception as e:
      raise ImageDataError(f"Failed to display image: {e}")
    