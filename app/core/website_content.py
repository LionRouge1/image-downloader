import requests
from bs4 import BeautifulSoup

class Content():
  def __init__(self, url):
    self.url = url
    
  def get_content(self):
    response = requests.get(self.url)
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
    
  def get_images(self):
    content = self.get_content()
    if content:
      # Find all image tags in the content
      images = content.find_all('img')
      # Extract the image URLs from the src attribute
      image_urls = [img['src'] for img in images if img.get('src') and img['src'].startswith(('http://', 'https://'))]
      # print(image_urls)
      return image_urls
    else:
      return None
    
  def __str__(self):
    return self.url