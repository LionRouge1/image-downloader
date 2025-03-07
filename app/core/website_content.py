import requests
from urllib.parse import urlparse, urljoin
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

class Content:
  def __init__(self, url, settings):
    self.url = url
    self.image_urls = []
    self.settings = settings
    self.max_images = int(self.settings.max_images)
    self.show_browser = self.settings.show_browser
    self.scheme = urlparse(url).scheme
    self.netloc = urlparse(url).netloc
    self.path = urlparse(url).path
    self.query = urlparse(url).query

  def scrape_images(self):
    with sync_playwright() as p:
      browser = p.chromium.launch(headless= not self.show_browser)
      page = browser.new_page()
      page.goto(self.url)
      page.wait_for_load_state(state="domcontentloaded", timeout=6000)
      images = page.query_selector_all("img")[:self.max_images]
      self.image_urls = [self.reconstruct_url(img.get_attribute("src")) for img in images if img.get_attribute("src")]

      if self.settings.get_css_images and len(self.image_urls) < self.max_images:
        max = self.max_images - len(images)
        css_images = page.evaluate('''(max) => {
          const images = [];
          for (const sheet of document.styleSheets) {
            try {
              for (const rule of sheet.cssRules) {
                if (rule.style && rule.style.backgroundImage) {
                  const match = rule.style.backgroundImage.match(/url\\(['"]?([^'"]+)['"]?\\)/);
                  if (match) {
                    if (images.length >= max) { break; }
                    images.push(match[1]);
                  }
                }
              }
            } catch (e) {
              console.warn("Could not access stylesheet:", e);
            }
          }
          return images;
        }''', max)

        self.image_urls += [self.reconstruct_url(img) for img in css_images if img]
      browser.close()

      return self.image_urls

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
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(self.url, headers=headers)
    content_type = response.headers.get('Content-Type')
    response.raise_for_status()

    if 'image' in content_type:
      return [self.url]
    
    content = BeautifulSoup(response.text, 'html.parser')
    

    if content:
      images = content.find_all('img')[:self.max_images]
      self.image_urls = [self.reconstruct_url(img['src']) for img in images if img.get('src')]

      if self.settings.get_css_images and len(self.image_urls) < self.max_images:
        css_files = content.find_all('link', rel='stylesheet')
        for css_file in css_files:
          css_url = self.reconstruct_url(css_file['href'])
          css_content = self.get_css_content(css_url)
          if css_content:
            self.extract_image_urls_from_css(css_content, css_url)
      
      return self.image_urls
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
    url_pattern = re.compile(r'background-image:\s*url\((.*?)\)')
    matches = url_pattern.findall(css_content)

    for match in matches:
      if len(self.image_urls) >= self.max_images:
        break

      match = match.strip('\'" ')
      full_url = urljoin(css_url, match)

      if self.is_valid_url(full_url):
        self.image_urls.append(full_url)
    
  def __str__(self):
    return self.url
