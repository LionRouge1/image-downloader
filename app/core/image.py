import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image
from decimal import Decimal
import cairosvg
import re
import os
from .setting import Settings

class ImageDataError(Exception):
  pass

class ImageData:
  def __init__(self, url):
    self.url = url
    self.output_directory = Settings().save_directory
    self.path = urlparse(url).path
    self.scheme = urlparse(url).scheme

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    self.response = requests.get(url, headers=headers)
    self.response.raise_for_status
    
    self.image_data = BytesIO(self.response.content)
    if self.path.lower().endswith('.svg'):
      self.format = 'SVG'
      self.size = "N/A"
      self.mode = "N/A"
      self.filename = self.image_name()
      self.image_data.seek(0)
      self.image = self.image_data.read()
    else:
      self.image = Image.open(self.image_data)
      self.format = self.image.format
      self.filename = self.image_name()
      self.size = self.image.size,
      self.mode = self.image.mode,

  def is_valid_image_name(self, name):
    return bool(re.match(r"^[\w\s_()-]+\.[A-Za-z]{3,4}$", name))

  def image_name(self):
    image_name = 'default_name'
    content_disposition = self.response.headers.get('Content-Disposition')

    if content_disposition:
      filename = re.findall('filename="(.+)"', content_disposition)
      if filename:
        image_name = filename[0]
    elif self.is_valid_image_name(self.path.split('/')[-1]):
      image_name = self.url.split('/')[-1]
    return image_name
  
  def get_file_size(self):
    number = Decimal(len(self.response.content) / (1024 * 1024))
    formatted_number = number.quantize(Decimal("0.001"))
    return formatted_number
  
  def image_properties(self):
    return {
      "format": self.format,
      "size": self.size,
      "filename": self.filename,
      "mode": self.mode,
      "file_size": self.get_file_size()
    }
  
  def display_image(self):
    try:
      if self.format == 'SVG':
        png_data = cairosvg.svg2png(bytestring=self.image)
        img = Image.open(BytesIO(png_data))
      else:
        img = self.image

      img = img.resize((200, 200), Image.NEAREST)  # Use Image.LANCZOS instead of Image.ANTIALIAS
      img_byte_arr = BytesIO()
      format = 'PNG' if self.format == 'SVG' else self.format
      img.save(img_byte_arr, format=format)
      img_byte_arr = img_byte_arr.getvalue()

      return img_byte_arr
    except Exception as e:
      raise ImageDataError(f"Failed to display image: {e}")
    
  def save_image(self):
    try:
      if not os.path.exists(self.output_directory):
        os.makedirs(self.output_directory, exist_ok=True)
      output_path = os.path.join(self.output_directory, self.filename)
      if self.format == 'SVG':
        with open(output_path, 'wb') as f:
          f.write(self.image_data.getvalue())
      else:
        self.image.save(output_path, format=self.format, quality=95, optimize=True, progressive=True, dpi=(300, 300), lossless=True)
    
    except Exception as e:
      raise ImageDataError(f"Failed to save image: {e}")
    