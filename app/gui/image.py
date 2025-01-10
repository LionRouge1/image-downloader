from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
  QWidget,
  QLabel,
  QPushButton,
  QVBoxLayout,
  QHBoxLayout,
  QComboBox
)
from ..core.image import ImageData
from .utils import show_success_message, show_error_message

class ImageThread(QThread):
  image_downloaded = pyqtSignal(object)
  thread_finished = pyqtSignal(bool)

  def __init__(self, url, settings):
    super().__init__()
    self.url = url
    self.settings = settings

  def run(self):
    try:
      image = ImageData(self.url, self.settings)
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
    self.thread = ImageThread(self.url, parent.settings)
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
      self.toggle_button = QPushButton("Details")
      self.toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)
      self.save_button = QPushButton("Save")
      self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
      self.save_button.setStyleSheet("background: green; color: white")
      self.save_button.clicked.connect(self.save_image)
      self.toggle_button.clicked.connect(self.toggle_details)

      self.format_combo = QComboBox()

      # self.image_box_layout = QVBoxLayout()
      self.button_widget = QWidget()
      self.button_layout = QHBoxLayout()
      self.button_layout.addStretch()
      self.button_widget.setLayout(self.button_layout)
      self.button_layout.addWidget(self.toggle_button)
      self.button_layout.addWidget(self.format_combo)
      self.button_layout.addWidget(self.save_button)

      self.details_label = QLabel()
      self.image_properties = self.image.image_properties()
      
      match self.image_properties['format']:
        case 'SVG':
          image_formats = ["SVG", "PNG", "WEBP"]
        case 'JPEG':
          image_formats = ["JPEG", "PNG", "WEBP", "BMP", "GIF", "ICO", "TIFF"]
        case _:
          image_formats = ["", "PNG", "JPEG", "WEBP", "BMP", "GIF", "ICO", "TIFF"]

      self.format_combo.addItems(image_formats)
      self.format_combo.setCurrentText(self.image_properties['format'])
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
    self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    self.image_box_layout.addWidget(self.label)


  def toggle_details(self):
    self.visibility_state = not self.visibility_state
    self.details_label.setVisible(self.visibility_state)
    self.toggle_button.setText("Hide" if self.visibility_state else "Details")

  def save_image(self):
    selected_format = self.format_combo.currentText()
    try:
      self.image.save_image(selected_format)
      show_success_message(f"Image has been successfully downloaded to {self.parent.settings.save_directory}")
    except Exception as e:
      show_error_message(str(e))
