import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image
from decimal import Decimal
import cairosvg
import re
import os
# from main import MainWindow
# from .settings import load_settings

class ImageDataError(Exception):
  pass

class ImageData():
  def __init__(self, url, settings):
    super().__init__()
    self.url = url
    self.path = urlparse(url).path
    self.scheme = urlparse(url).scheme
    self.settings = settings
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    self.response = requests.get(url, headers=headers)
    self.response.raise_for_status
    self.filename = self.image_name()
    self.image_name_without_extension = self.filename.split('.')[0]
    self.file_directory = self.settings.save_directory
    # self.output_path = os.path.join(self.file_directory, self.filename)
    
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

  def output_path(self, format):
    return os.path.join(self.file_directory, f"{self.image_name_without_extension}.{format.lower()}")
  
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
          case 'JPEG':
            self.save_svg_to_jpeg()
          case 'WEBP':
            self.save_svg_to_webp()
          case _:
            with open(output_path, 'wb') as f:
              f.write(self.image_data.getvalue())
      else:
        image_format = format or self.format
        self.image.save(self.output_path(image_format), format=image_format, quality=95, optimize=True, progressive=True, dpi=(300, 300), lossless=True)
    