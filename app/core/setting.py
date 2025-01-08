import os
from pathlib import Path
import json

# def get_download_folder():
#   """Get the default Downloads folder for the current OS."""
#   if os.name == 'nt':  # Windows
#     return str(Path.home() / "Downloads")
#   elif os.name == 'posix':  # macOS or Linux
#     return str(Path.home() / "Downloads")
#   else:
#     raise NotImplementedError("OS not supported")

# def load_settings():
#   default_directory = os.path.join(get_download_folder(), "downloader_images")
#   settings = {
#     'save_directory': default_directory,
#     'image_format': 'jpg',
#     'max_images': 50,
#     'get_css_images': False
#   }
#   if os.path.exists('settings.json'):
#     with open('settings.json', 'r') as json_file:
#       settings_dict = json.load(json_file)
#       settings['save_directory'] = settings_dict.get('save_directory', default_directory)
#       settings['image_format'] = settings_dict.get('image_format', 'jpg')
#       settings['max_images'] = settings_dict.get('max_images', 50)
#       settings['get_css_images'] = settings_dict.get('get_css_images', False)
#   return settings

# def save_settings(new_directory, max_images, get_css_images):
#   settings_dict = {
#     'save_directory': new_directory,
#     'image_format': 'jpg',
#     'max_images': max_images,
#     'get_css_images': get_css_images
#   }
#   with open('settings.json', 'w') as json_file:
#     json.dump(settings_dict, json_file, indent=2)

class Settings:
  def __init__(self):
    self.default_directory = os.path.join(self.get_download_folder(), "downloader_images")
    self.save_directory = self.default_directory
    self.image_format = ''
    self.max_images = 50
    self.get_css_images = True
    self.load_settings()

  def load_settings(self):
    if os.path.exists('settings.json'):
      with open('settings.json', 'r') as json_file:
        settings_dict = json.load(json_file)
        self.save_directory = settings_dict.get('save_directory', self.default_directory)
        self.image_format = settings_dict.get('image_format', 'jpg')
        self.max_images = settings_dict.get('max_images', 50)
        self.get_css_images = settings_dict.get('get_css_images', False)

  def create_save_directory(self):
    if not os.path.exists(self.get_download_folder()):
      os.makedirs(self.default_directory, exist_ok=True)

  def update_save_directory(self, new_directory):
    if os.path.exists(new_directory):
      self.save_directory = new_directory
    else:
      raise ValueError(f"The directory {new_directory} does not exist.")

  def update_image_format(self, new_format):
    if new_format in ['jpg', 'png', 'gif']:
      self.image_format = new_format
    else:
      raise ValueError("Invalid image format. Choose from 'jpg', 'png', 'gif'.")

  def update_max_images(self, new_max):
    if isinstance(new_max, int) and new_max > 0:
      self.max_images = new_max
    else:
      raise ValueError("Max images must be a positive integer.")
    
  def enable_css_images(self):
    self.get_css_images = True

  def get_download_folder(self):
    """Get the default Downloads folder for the current OS."""
    if os.name == 'nt':  # Windows
      return str(Path.home() / "Downloads")
    elif os.name == 'posix':  # macOS or Linux
      return str(Path.home() / "Downloads")
    else:
      raise NotImplementedError("OS not supported")
    
  def save_settings(self, new_directory, max_images, get_css_images):
    settings_dict = {
      'save_directory': new_directory,
      'image_format': self.image_format,
      'max_images': max_images,
      'get_css_images': get_css_images
    }
    with open('settings.json', 'w') as json_file:
      json.dump(settings_dict, json_file, indent=2)

    self.load_settings()
