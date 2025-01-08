from PyQt6.QtCore import Qt, QThread, pyqtSignal
from ..core.website_content import Content
from ..core.history import History
from PyQt6.QtWidgets import (
  QWidget,
  QLabel,
  QPushButton,
  QVBoxLayout,
  QHBoxLayout,
  QScrollArea,
  QGridLayout
)
from .image import ImageWidget
from .utils import show_success_message, show_error_message
from .animation import Spinner 

class ImagesLoaderThread(QThread):
  urls_loaded = pyqtSignal(list)
  error_occurred = pyqtSignal(str)

  def __init__(self, url, settings):
    super().__init__()
    self.url = url
    self.settings = settings

  def run(self):
    try:
      web_content = Content(self.url, self.settings)
      images_url = web_content.scrape_images() if self.settings.simulate else web_content.get_images()

      if images_url:
        self.urls_loaded.emit(images_url)
      else:
        self.error_occurred.emit("No images found on the website.")
    except Exception as e:
      # show_error_message(f"Failed to load images: {e}")
      self.error_occurred.emit(f"Failed to load Website content")

class ImagesWindow(QWidget):
  def __init__(self, url, settings):
    super().__init__()
    self.settings = settings
    self.url = url
    self.history = History()
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

    self.thread = ImagesLoaderThread(url, settings)
    self.thread.urls_loaded.connect(self.display_images)
    self.thread.error_occurred.connect(self.display_error_message)
    self.thread.start()
    self.thread.finished.connect(lambda: self.loading_widget.hide())

    self.grid_layout = QGridLayout()
    self.images_widget.setLayout(self.grid_layout)
    layout.addWidget(scroll_area)
  
  def display_images(self, images_url):
    row, col = 0, 0
    for url in images_url:
      image_widget = ImageWidget(url, self)
      self.grid_layout.addWidget(image_widget, row, col)
      col += 1
      if col == 5:
        row += 1
        col = 0

    self.history.add_to_history(self.url, images_url)

  def display_error_message(self, message):
    self.label.setText('')
    error_label = QLabel(message)
    error_label.setWordWrap(True)
    error_label.setStyleSheet('color: red')
    self.grid_layout.addWidget(error_label, 0, 0)

  def download_all_images(self):
    self.download_all.setDisabled(True)
    for image in self.images:
      if image:
        image.save_image()
    
    show_success_message('All images have been successfully downloaded.')
    self.download_all.setDisabled(False)
