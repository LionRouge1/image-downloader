import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image
from decimal import Decimal
import base64
import cairosvg
import re
import os

class ImageDataError(Exception):
  pass

class ImageData():
  def __init__(self, url, settings):
    super().__init__()
    self.url = url
    self.path = urlparse(url).path
    self.scheme = urlparse(url).scheme
    self.settings = settings
    self.file_directory = self.settings.save_directory
    
    if self.url.startswith('data:image'):
      self.decode_base64_image()
    else:
      self.get_image_from_url()

    self.filename = self.image_name()
    self.image_name_without_extension = self.filename.split('.')[0]

  def get_image_from_url(self):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    self.response = requests.get(self.url, headers=headers)
    self.response.raise_for_status
    self.image_data = BytesIO(self.response.content)
    if self.path.lower().endswith('.svg'):
      self.format = 'SVG'
      self.size = "N/A"
      self.mode = "N/A"
      self.image_data.seek(0)
      self.image = self.image_data.read()
    else:
      self.image = Image.open(self.image_data)
      self.format = self.image.format
      self.size = self.image.size,
      self.mode = self.image.mode,
  
  def decode_base64_image(self):
    self.response = None
    format = self.get_image_format_from_uri()
    # print(format)
    base64_string = self.url.split(",")[1]
    if format:
      self.format = format
      self.image = Image.open(BytesIO(base64.b64decode(base64_string)))
      self.size = self.image.size
      self.mode = self.image.mode
    else:
      raise ImageDataError("Invalid base64 image format")

  def get_image_format_from_uri(self):
    match = re.match(r"^data:image/(\w+);base64,", self.url)
    if match:
        return match.group(1).upper()
    return None
  
  def output_path(self, format):
    return os.path.join(self.file_directory, f"{self.image_name_without_extension}.{format.lower()}")
  
  def is_valid_image_name(self, name):
    return bool(re.match(r"^[\w\s_()-]+\.[A-Za-z]{3,4}$", name))

  def image_name(self):
    image_name = f"image_{id(self)}"
    if self.response:
      content_disposition = self.response.headers.get('Content-Disposition')
      if content_disposition:
        filename = re.findall('filename="(.+)"', content_disposition)
        if filename:
          image_name = filename[0]
      elif self.is_valid_image_name(self.path.split('/')[-1]):
        image_name = self.url.split('/')[-1]

    return image_name
  
  def get_file_size(self):
    formatted_number = "N/A"
    if self.response:
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
  
  def save_svg_to_png(self):
    cairosvg.svg2png(bytestring=self.image, write_to=self.output_path("PNG"))

  def save_svg_to_webp(self):
    png_data = cairosvg.svg2png(bytestring=self.image)
    img = Image.open(BytesIO(png_data))
    img.save(self.output_path("WEBP"), format="WEBP", quality=95, optimize=True, progressive=True, dpi=(300, 300), lossless=True)

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
    
  def save_image(self, format):
      file_directory = self.settings.save_directory
      if not os.path.exists(file_directory):
        os.makedirs(file_directory, exist_ok=True)
      output_path = os.path.join(file_directory, self.filename)
      if self.format == 'SVG':
        match format:
          case 'PNG':
            self.save_svg_to_png()
          case 'WEBP':
            self.save_svg_to_webp()
          case _:
            with open(output_path, 'wb') as f:
              f.write(self.image_data.getvalue())
      else:
        image_format = format or self.format
        if image_format.upper() == 'JPEG' and self.image.mode in ['RGBA', 'P']:
            self.image = self.image.convert('RGB')
        save_params = {
            'format': image_format,
            'quality': 95,
            'optimize': True,
            'progressive': True,
            'dpi': (300, 300)
        }
        if image_format.upper() not in ['JPEG', 'GIF']:
            save_params['lossless'] = True
        self.image.save(self.output_path(image_format), **save_params)
