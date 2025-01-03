import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import re

class Content():
  def __init__(self, url):
    self.url = url
    self.scheme = urlparse(url).scheme
    self.netloc = urlparse(url).netloc
    self.path = urlparse(url).path
    self.query = urlparse(url).query
    
  def get_content(self):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(self.url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
      
      # Return the content of the response
    print("Content got successfully")
    return BeautifulSoup(response.text, 'html.parser')
    # try:
    #   # Send a GET request to the URL
    #   response = requests.get(self.url)
    #   response.raise_for_status()  # Raise an exception for HTTP errors
      
    #   # Return the content of the response
    #   print("Content got successfully")
    #   return BeautifulSoup(response.text, 'html.parser')
    # except requests.exceptions.RequestException as e:
    #   print(f"Failed to retrieve content: {e}")
    #   return None

  def reconstruct_url(self, src):
    if src.startswith('//'):
      return f"{self.scheme}:{src}"
    elif src.startswith('/'):
      return f"{self.scheme}://{self.netloc}{src}"
    else:
      return src
    
  def is_valid_url(self, url):
    return bool(re.match(r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", url))
    
  def get_images(self):
    content = self.get_content()
    if content:
      # Find all image tags in the content
      images = content.find_all('img')
      # Extract the image URLs from the src attribute
      image_urls = [self.reconstruct_url(img['src']) for img in images if img.get('src')]
      # print(image_urls)

      css_files = content.find_all('link', rel='stylesheet')
      for css_file in css_files:
        css_url = self.reconstruct_url(css_file['href'])
        css_content = self.get_css_content(css_url)
        if css_content:
          css_image_urls = self.extract_image_urls_from_css(css_content, css_url)
          image_urls.extend(css_image_urls)
      return image_urls
    else:
      return None
    
  def get_css_content(self, css_url):
    try:
      response = requests.get(css_url)
      response.raise_for_status()
      return response.text
    except requests.RequestException as e:
      print(f"Failed to retrieve CSS content: {e}")
      return None

  def extract_image_urls_from_css(self, css_content, css_url):
    # Regular expression to find URLs in CSS content
    url_pattern = re.compile(r'background-image:\s*url\((.*?)\)')
    matches = url_pattern.findall(css_content)
    image_urls = []
    for match in matches:
      # Remove quotes and whitespace
      match = match.strip('\'" ')
      # Reconstruct the full URL
      full_url = urljoin(css_url, match)
      if self.is_valid_url(full_url):
        image_urls.append(full_url)
    return image_urls
    
  def __str__(self):
    return self.url
