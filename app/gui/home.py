from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import (
  QLineEdit,
  QWidget,
  QLabel,
  QPushButton,
  QVBoxLayout,
  QHBoxLayout
)
from .images import ImagesWindow
from .utils import show_error_message

class HomeWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.main_layout = QVBoxLayout()
    self.setLayout(self.main_layout)

    search_label = QLabel("Enter Website URL:")
    self.url_input = QLineEdit()
    url_regex = QRegularExpression(r"^(https?|ftp)://[^\s/$.?#].[^\s]*$")
    validator = QRegularExpressionValidator(url_regex, self.url_input)
    self.url_input.setValidator(validator)
    self.url_input.setPlaceholderText("https://www.example.com")
    self.url_input.setStyleSheet("height: 20px; padding: 10px")
    self.url_input.setMaximumWidth(400)

    self.search_btn = QPushButton("Search")
    self.search_btn.setStyleSheet("height: 20px; padding: 10px")

    search_layout = QHBoxLayout()
    search_layout.addWidget(search_label)
    search_layout.addWidget(self.url_input)
    search_layout.addWidget(self.search_btn)
    search_layout.addStretch()

    search_widget = QWidget()
    search_widget.setLayout(search_layout)
    search_widget.setMaximumWidth(600)

    self.main_layout.addWidget(search_widget)
    self.search_btn.clicked.connect(self.show_images)
    self.main_layout.addStretch()
    self.setStyleSheet("font-size: 16px; font-family: Arial;")
    

  def show_images(self):
    url = self.url_input.text()
    self.search_btn.setDisabled(True)
    try:

      images = ImagesWindow(url)
      self.main_layout.addWidget(images)

    except Exception as e:
      print("Error:", e)
      show_error_message(str(e))
    finally:
      self.search_btn.setDisabled(False)
      self.url_input.clear()
