from PyQt6.QtCore import Qt, QThread, pyqtSignal
from ..core.website_content import Content
from .image import ImageWidget
from .utils import show_success_message, show_error_message
from .animation import Spinner 

from PyQt6.QtWidgets import (
  QWidget,
  QLabel,
  QPushButton,
  QVBoxLayout,
  QHBoxLayout,
  QScrollArea,
  QGridLayout
)

class ImagesLoaderThread(QThread):
  urls_loaded = pyqtSignal(list)

  def __init__(self, url):
    super().__init__()
    self.url = url

  def run(self):
    try:
      web_content = Content(self.url)
      images_url = web_content.get_images()
      self.urls_loaded.emit(images_url)
    except Exception as e:
      show_error_message(f"Failed to load images: {e}")

class ImagesWindow(QWidget):
  def __init__(self, url):
    super().__init__()

    self.images = []
    self.label = QLabel("Here are the images from the website:")
    self.download_all = QPushButton("Download All")
    self.download_all.clicked.connect(self.download_all_images)
    self.download_all.setStyleSheet("background: green; color: white")
    self.download_all.setCursor(Qt.CursorShape.PointingHandCursor)

    clear_button = QPushButton("Clear")
    clear_button.setStyleSheet("background: red; color: white")
    clear_button.setCursor(Qt.CursorShape.PointingHandCursor)
    clear_button.clicked.connect(lambda: self.close())

    f_widget = QWidget()
    f_layout = QHBoxLayout()
    f_widget.setLayout(f_layout)
    f_layout.addStretch()
    f_layout.addWidget(self.label)
    f_layout.addWidget(self.download_all)
    f_layout.addWidget(clear_button)

    layout = QVBoxLayout()
    layout.addStretch()
    self.setLayout(layout)
    layout.addWidget(f_widget)

    scroll_area = QScrollArea()
    scroll_area.setMinimumHeight(500)
    scroll_area.setWidgetResizable(True)

    self.images_widget = QWidget()
    scroll_area.setWidget(self.images_widget)

    self.loading_layout = QHBoxLayout()
    self.loading_widget = QWidget()

    self.spinner = Spinner()
    self.spinner.setFixedSize(40, 40)
    self.loading_widget.setLayout(self.loading_layout)
    self.loading_layout.addStretch()
    loading_label = QLabel("Downloading images...")
    self.loading_layout.addWidget(self.spinner)
    self.loading_layout.addWidget(loading_label)

    layout.addWidget(self.loading_widget)
    # self.loading_widget.hide()

    self.thread = ImagesLoaderThread(url)
    self.thread.urls_loaded.connect(self.display_images)
    self.thread.start()

    self.grid_layout = QGridLayout()
    self.images_widget.setLayout(self.grid_layout)
    layout.addWidget(scroll_area)

  
  def display_images(self, images_url):
    row, col = 0, 0
    for url in images_url:
      try:
        image_widget = ImageWidget(url)
        self.images.append(image_widget.image)
        self.grid_layout.addWidget(image_widget, row, col)
      except Exception as e:
        show_error_message(f"Failed to load image from {url}: {e}")

      col += 1
      if col == 5:
        row += 1
        col = 0
    
    self.loading_widget.hide()

  def download_all_images(self):
    self.download_all.setDisabled(True)
    for image in self.images:
      image.save_image()
    
    show_success_message('All images have been successfully downloaded.')
    self.download_all.setDisabled(False)
