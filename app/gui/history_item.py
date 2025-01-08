from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from .view_history import ViewHistoryUI

class HistoryItemUI(QWidget):
  def __init__(self, tab, history, history_object, settings):
    super().__init__()
    self.layout = QHBoxLayout(self)
    self.tab_widget = tab
    # self.settings = settings
    self.label_url = QLabel(history['url'])
    self.label_url.setWordWrap(True)
    self.label_url.setStyleSheet("font-size: 16px; font-family: Arial")
    self.label_date = QLabel(history['timestamp'])
    self.label_date.setStyleSheet("font-size: 16px; font-family: Arial")

    view_button = QPushButton("View")
    view_button.clicked.connect(lambda _, tab=self.tab_widget, ht=history, obj = history_object, set=settings: self.update_history_tab(tab, ht, obj, set))
    view_button.setStyleSheet("background: green; color: white; padding: 8px")
    view_button.setCursor(Qt.CursorShape.PointingHandCursor)
    view_button.setFixedWidth(80)

    delete_button = QPushButton("Delete")
    delete_button.clicked.connect(lambda _, id=history['id'], callback=history_object.delete_from_history: self.delete_history(id, callback))
    delete_button.setStyleSheet("background: red; color: white; padding: 8px")
    delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
    delete_button.setFixedWidth(80)
        
    self.layout.addWidget(self.label_url)
    self.layout.addWidget(self.label_date)
    self.layout.addWidget(view_button)
    self.layout.addWidget(delete_button)

  def update_history_tab(self, tab, history, object, setting):
    ViewHistoryUI(tab, history, object.view_history, setting)

  def delete_history(self, id, callback):
    callback(id)

    self.setParent(None)
    self.deleteLater()
