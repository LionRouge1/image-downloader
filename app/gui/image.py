from PyQt6.QtCore import *
from PyQt6.QtGui import *
from ..core.image import ImageData

from PyQt6.QtWidgets import *

class ImageWidget(QWidget):
  def __init__(self, url):
    super().__init__()
    self.url = url
    self.visibility_state = False
    self.image = ImageData(url)
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
    self.image_box_layout = QVBoxLayout()
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
    self.setLayout(self.image_box_layout)

  def toggle_details(self):
    self.visibility_state = not self.visibility_state
    self.details_label.setVisible(self.visibility_state)
    self.toggle_button.setText("Hide Details" if self.visibility_state else "Show Details")

  def save_image(self):
    self.image.save_image()

    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setText("Image has been successfully downloaded.")
    msg_box.setWindowTitle("Download Complete")
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()

