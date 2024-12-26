import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QRegularExpression, Qt
from PyQt6.QtGui import QRegularExpressionValidator, QIcon, QPixmap
from ..core.website_content import Content
from .images import ImagesWindow
import os


def show_images(url_input, layout):
  global images_src
  url = url_input.text()
  try:
    loading_label = QLabel("Loading images...")
    layout.addWidget(loading_label)
    QApplication.processEvents()

    images = ImagesWindow(url)
    layout.addWidget(images)

  except Exception as e:
    print("Error:", e)
    show_error_message(str(e))
  finally:
    loading_label.deleteLater()

def show_error_message(message):
  msg_box = QMessageBox()
  msg_box.setIcon(QMessageBox.Icon.Critical)
  msg_box.setText("Error")
  msg_box.setInformativeText(message)
  msg_box.setWindowTitle("Error")
  msg_box.exec()

def window():
  app = QApplication(sys.argv)
  win = QWidget()

  icon_path = "/home/crowdfrica/Matchoudi/image-downloader/app/gui/assets/logo.png"
  icon = QIcon(icon_path)
  win.setWindowIcon(icon)

  label = QLabel("Enter Website URL:")
  url_input = QLineEdit()
  url_regex = QRegularExpression(r"^(https?|ftp)://[^\s/$.?#].[^\s]*$")
  validator = QRegularExpressionValidator(url_regex, url_input)
  url_input.setValidator(validator)
  url_input.setPlaceholderText("https://www.example.com")
  url_input.setStyleSheet("height: 20px; padding: 10px")
  url_input.setMaximumWidth(400)

  search_btn = QPushButton("Search")
  search_btn.setStyleSheet("height: 20px; padding: 10px")

  search_box = QHBoxLayout()
  search_box.addWidget(label)
  search_box.addWidget(url_input)
  search_box.addWidget(search_btn)

  search_box_container = QWidget()
  search_box_container.setLayout(search_box)
  search_box_container.setMaximumWidth(600)

  center_layout = QHBoxLayout()
  center_layout.addStretch()
  center_layout.addWidget(search_box_container)
  center_layout.addStretch()
  
  main_layout = QVBoxLayout()
  main_layout.addWidget(search_box_container)
  search_btn.clicked.connect(lambda: show_images(url_input, main_layout))
  main_layout.addStretch()

  win.setLayout(main_layout)
  win.setStyleSheet("font-size: 16px; font-family: Arial;")
  win.setMinimumWidth(700)
  win.setWindowTitle("Images Downloader")
  win.show()
  sys.exit(app.exec())

if __name__ == "__main__":
  window()