from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
  QWidget,
  QLabel,
  QVBoxLayout,
  QScrollArea,
  QGridLayout
)
from ..core.history import History

class HistoryLoaderThread(QThread):
  history_loaded = pyqtSignal(object)
  error_occurred = pyqtSignal(str)

  def __init__(self):
    super().__init__()

  def run(self):
    try:
      history = History()
      self.history_loaded.emit(history)
    except Exception as e:
      self.error_occurred.emit(f"Failed to load History: {e}")

class HistoryUI(QWidget):
  def __init__(self):
    super().__init__()
    self.main_layout = QVBoxLayout()
    self.setLayout(self.main_layout)
    self.label = QLabel("Here is the history of your downloads:")

    self.history_widget = QWidget()
    scroll_area = QScrollArea()
    scroll_area.setMinimumHeight(500)
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(self.history_widget)

    self.grid_layout = QGridLayout()
    self.history_widget.setLayout(self.grid_layout)

    self.thread = HistoryLoaderThread()
    self.thread.history_loaded.connect(self.populate_history)
    self.thread.start()
    self.main_layout.addWidget(self.label)
    self.main_layout.addWidget(scroll_area)

  def populate_history(self, history):
    for index, item in enumerate(history.history):
      url_label = QLabel(item['url'])
      date_label = QLabel(item['timestamp'])
      self.grid_layout.addWidget(url_label, index, 0)
      self.grid_layout.addWidget(date_label, index, 1)