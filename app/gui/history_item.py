from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from .view_history import ViewHistoryUI

class HistoryItemUI(QWidget):
  def __init__(self, tab, history, history_object):
    super().__init__()
    # self.history_entry = history_entry
    self.layout = QHBoxLayout(self)
    self.tab_widget = tab
        
    self.label_url = QLabel(history['url'])
    self.label_date = QLabel(history['timestamp'])

    view_button = QPushButton("View")
    view_button.clicked.connect(lambda _, tab=self.tab_widget, ht=history, obj = history_object: self.update_history_tab(tab, ht, obj))

    delete_button = QPushButton("Delete")
    delete_button.clicked.connect(lambda _, id=history['id'], callback=history_object.delete_from_history: self.delete_history(id, callback))
        
    self.layout.addWidget(self.label_url)
    self.layout.addWidget(self.label_date)
    self.layout.addWidget(view_button)
    self.layout.addWidget(delete_button)

  def update_history_tab(self, tab, history, object):
    ViewHistoryUI(tab, history, object.view_history)

  def delete_history(self, id, callback):
    callback(id)

    self.setParent(None)
    self.deleteLater()
