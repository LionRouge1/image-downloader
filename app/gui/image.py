from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
  QWidget,
  QLabel,
  QPushButton,
  QVBoxLayout,
  QHBoxLayout
)
from ..core.image import ImageData
from .utils import show_success_message, show_custom_error_message

class ImageThread(QThread):
  image_downloaded = pyqtSignal(object)
  thread_finished = pyqtSignal(bool)

  def __init__(self, url):
    super().__init__()
    self.url = url

  def run(self):
    try:
      image = ImageData(self.url)
      self.image_downloaded.emit(image)
    except Exception as e:
      self.thread_finished.emit(False)

class ImageWidget(QWidget):
  def __init__(self, url, parent=None):
    super().__init__()
    self.url = url
    self.parent = parent
    self.visibility_state = False
    self.image_box_layout = QVBoxLayout()
    self.setLayout(self.image_box_layout)
    self.setMaximumWidth(250)
    self.image = None
    self.thread = ImageThread(self.url)
    self.thread.image_downloaded.connect(self.add_image)
    self.thread.thread_finished.connect(self.on_thread_finished)
    self.thread.start()

  def add_image(self, image):
    if image:
      self.parent.images.append(image)
      # print(self.parent.images)
      self.image = image
      self.pixmap = QPixmap()
      self.pixmap.loadFromData(self.image.display_image())
      self.image_label = QLabel()
      self.image_label.setPixmap(self.pixmap)
      self.image_label.setScaledContents(True)
      self.toggle_button = QPushButton("Show Details")
      self.toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)
      self.save_button = QPushButton("Save Image")
      self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
      self.save_button.setStyleSheet("background: green; color: white")
      self.save_button.clicked.connect(self.save_image)
      self.toggle_button.clicked.connect(self.toggle_details)
      # self.image_box_layout = QVBoxLayout()
      self.button_widget = QWidget()
      self.button_layout = QHBoxLayout()
      self.button_layout.addStretch()
      self.button_widget.setLayout(self.button_layout)
      self.button_layout.addWidget(self.toggle_button)
      self.button_layout.addWidget(self.save_button)

      self.details_label = QLabel()
      self.image_properties = self.image.image_properties()
      self.details_label.setText(
        f"Image Name: {self.image_properties['filename']}\n"
        f"Image Size: {self.image_properties['size']}\n"
        f"Image Format: {self.image_properties['format']}\n"
        f"File Size: {self.image_properties['file_size']} MB\n"
      )
      self.details_label.setVisible(self.visibility_state)
      self.image_box_layout.addWidget(self.image_label)
      self.image_box_layout.addWidget(self.button_widget)
      self.image_box_layout.addWidget(self.details_label)
  
  def on_thread_finished(self, status):
      self.label = QLabel()
      self.label.setScaledContents(True)
      self.label.setWordWrap(True)
      self.label.setText(
        f"Failed to load image from: {self.url}"
      )
      self.image_box_layout.addWidget(self.label)


  def toggle_details(self):
    self.visibility_state = not self.visibility_state
    self.details_label.setVisible(self.visibility_state)
    self.toggle_button.setText("Hide Details" if self.visibility_state else "Show Details")

  def save_image(self):
    self.image.save_image()

    show_success_message("Image has been successfully downloaded.")

