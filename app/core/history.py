import os
import json
from datetime import datetime

class History:
  def __init__(self):
    self.histories = []
    self.load_history()

  def load_history(self):
    if os.path.exists('history.json'):
      with open('history.json', 'r') as json_file:
        self.histories = json.load(json_file)

  def add_to_history(self, url, images=[]):
    website = {
      "id": 1,
      "url": url,
      "images": images,
      "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    histories = [website]
    # self.histories.insert(0, website)
    for index, website in enumerate(self.histories):
      if website['url'] != url:
        website['id'] = index + 2
        histories.append(website)
    self.histories = histories
    self.save_history()

  def save_history(self):
    with open('history.json', 'w') as json_file:
      json.dump(self.histories, json_file, indent=2)

  def delete_from_history(self, website_id):
    self.histories = [website for website in self.histories if website['id'] != website_id]
    for index, website in enumerate(self.histories):
      website['id'] = index + 1

    self.save_history()

  def clear_history(self):
    self.histories = []
    self.save_history()

  def get_histories(self):
    return self.histories
  
  def get_history(self, website_id):
    for website in self.histories:
      if website['id'] == website_id:
        return website
      
  def view_history(self, website_id):
    history = self.get_history(website_id)
    if history:
      history = {
        "id": 1,
        "url": history['url'],
        "images": history['images'],
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      }
      histories = [history]
      for index, website in enumerate(self.histories):
        if website['id'] != website_id:
          website['id'] = index + 2
          histories.append(website)
      self.histories = histories
      self.save_history()


  def get_history_count(self):
    return len(self.history)