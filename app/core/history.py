import os
import json
from datetime import datetime

class History:
  def __init__(self):
    self.history = []
    self.load_history()

  def load_history(self):
    if os.path.exists('history.json'):
      with open('history.json', 'r') as json_file:
        self.history = json.load(json_file)

  def add_to_history(self, url, images=[]):
    website = {
      "id": len(self.history) + 1,
      "url": url,
      "images": images,
      "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    self.history.append(website)
    self.save_history()

  def save_history(self):
    with open('history.json', 'w') as json_file:
      json.dump(self.history, json_file, indent=2)

  def delete_from_history(self, website_id):
    self.history = [website for website in self.history if website['id'] != website_id]
    self.save_history()

  def clear_history(self):
    self.history = []
    self.save_history()

  def get_history(self):
    return self.history

  def get_history_count(self):
    return len(self.history)