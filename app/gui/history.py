from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtWidgets import (
  QWidget,
  QVBoxLayout,
  QScrollArea,
  QFormLayout,
  QGroupBox,
  QPushButton,
  QMessageBox,
  QHBoxLayout,
  QLabel
)
from ..core.history import History
from .history_item import HistoryItemUI

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
  def __init__(self, tab_widget, settings):
    super().__init__()
    self.main_layout = QVBoxLayout(self)
    self.tab_widget = tab_widget
    self.history = None
    self.settings = settings

    self.form_layout = QFormLayout()
    self.group_box = QGroupBox("Here is the history of your downloads")
    self.group_box.setLayout(self.form_layout)

    self.clear_button = QPushButton("Clear History")
    self.clear_button.clicked.connect(self.clear_history)
    self.clear_button.setStyleSheet("background: red; color: white; padding: 8px")
    self.clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
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

    while self.form_layout.count():
      child = self.form_layout.takeAt(0)
      if child.widget():
        child.widget().deleteLater()

    header_widget = QWidget()
    header_layout = QHBoxLayout(header_widget)
    button_style = "font-size: 18px; font-family: Arial; font-weight: bold; padding: 5px; border: 1px solid #ccc;"
    website_button = QLabel("Website URL")
    website_button.setStyleSheet(button_style)
    website_button.setAlignment(Qt.AlignmentFlag.AlignCenter)
    date_button = QLabel("Date")
    date_button.setStyleSheet(button_style)
    date_button.setAlignment(Qt.AlignmentFlag.AlignCenter)
    actions_button = QLabel("Actions")
    actions_button.setStyleSheet(button_style)
    actions_button.setAlignment(Qt.AlignmentFlag.AlignCenter)

    header_layout.addWidget(website_button)
    header_layout.addWidget(date_button)
    header_layout.addWidget(actions_button)
    self.form_layout.addRow(header_widget)

    for index, item in enumerate(history.get_histories()):
      row = HistoryItemUI(self.tab_widget, item, history, self.settings)
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
      while self.form_layout.count():
        child = self.form_layout.takeAt(0)
        if child.widget():
          child.widget().deleteLater()
      self.populate_history(self.history)
