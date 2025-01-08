from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
  QWidget,
  QVBoxLayout,
  QScrollArea,
  QFormLayout,
  QGroupBox,
  QPushButton,
  QMessageBox
)
from ..core.history import History
from .history_item import HistoryItemUI
from .view_history import ViewHistoryUI

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
  def __init__(self, tab_widget):
    super().__init__()
    self.main_layout = QVBoxLayout(self)
    self.tab_widget = tab_widget
    self.history = None

    self.form_layout = QFormLayout()
    self.group_box = QGroupBox("Here is the history of your downloads:")
    self.group_box.setLayout(self.form_layout)

    self.clear_button = QPushButton("Clear History")
    self.clear_button.clicked.connect(self.clear_history)
    self.clear_button.setStyleSheet("background: red; color: white; padding: 8px")
    self.main_layout.addWidget(self.clear_button)

    scroll_area = QScrollArea()
    scroll_area.setMinimumHeight(500)
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(self.group_box)

    self.thread = HistoryLoaderThread()
    self.thread.history_loaded.connect(self.populate_history)
    self.thread.start()
    self.main_layout.addWidget(scroll_area)

  def populate_history(self, history):
    self.history = history
    for index, item in enumerate(history.get_histories()):
      row = HistoryItemUI(self.tab_widget, item, history)
      self.form_layout.addRow(row)

  def clear_history(self):
    confirmation = QMessageBox.question(
      self,
      "Clear History",
      "You about to clear all the history. Do you still want to proceed ?",
      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )

        # If the user confirms, delete the widget
    if confirmation == QMessageBox.StandardButton.Yes:

      self.history.clear_history()
      self.form_layout.deleteLater()
      self.populate_history(self.history)

