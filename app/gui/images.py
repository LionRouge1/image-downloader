from PyQt6.QtCore import *
from PyQt6.QtGui import *
from ..core.website_content import Content
from .image import ImageWidget

from PyQt6.QtWidgets import *

class ImagesWindow(QWidget):
  def __init__(self, url):
    super().__init__()
    if self.parent():
      self.parent().layout().removeWidget(self)

    self.images = []
    self.label = QLabel("Here are the images from the website:")
    download_all = QPushButton("Download All")
    download_all.setStyleSheet("background: green; color: white")
    download_all.setCursor(Qt.CursorShape.PointingHandCursor)

    clear_button = QPushButton("Clear")
    clear_button.setStyleSheet("background: red; color: white")
    clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
    clear_button.clicked.connect(lambda: self.close())

    f_widget = QWidget()
    f_layout = QHBoxLayout()
    f_widget.setLayout(f_layout)
    f_layout.addStretch()
    f_layout.addWidget(self.label)
    f_layout.addWidget(download_all)
    f_layout.addWidget(clear_button)

    layout = QVBoxLayout()
    layout.addStretch()
    self.setLayout(layout)
    layout.addWidget(f_widget)

    scroll_area = QScrollArea()
    scroll_area.setMinimumHeight(500)
    scroll_area.setWidgetResizable(True)
    # scroll_area.setStyleSheet("background: white; border: 1px solid black; border-radius: 5px; padding: 10px")

    images_widget = QWidget()
    scroll_area.setWidget(images_widget)
    # images_widget.setStyleSheet("background: white; border: 1px solid black; border-radius: 5px; padding: 10px")

    web_content = Content(url)
    images_url = web_content.get_images()
    download_all.clicked.connect(self.download_all_images)

    grid_layout = QGridLayout()
    images_widget.setLayout(grid_layout)
    layout.addWidget(scroll_area)
    row, col = 0, 0

    for url in images_url:
      image_widget = ImageWidget(url)
      self.images.append(image_widget.image)
      grid_layout.addWidget(image_widget, row, col)
      col += 1
      if col == 5:
        row += 1
        col = 0

  def download_all_images(self):
    for image in self.images:
      image.save_image()

    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setText("All images have been successfully downloaded.")
    msg_box.setWindowTitle("Download Complete")
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()
