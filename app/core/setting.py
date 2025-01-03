import os

class Settings:
  def __init__(self, save_directory=None, image_format='jpg', max_images=100):
    self.save_directory = save_directory or os.path.join(os.getcwd(), 'images')
    self.image_format = image_format
    self.max_images = max_images
    self.get_css_images = False

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

# Example usage
# settings = Settings()
# settings.update_save_directory('/path/to/new/directory')
# settings.update_image_format('png')
# settings.update_max_images(50)