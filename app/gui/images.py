import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from ..core.website_content import Content
from ..core.image import ImageData

from PyQt6.QtWidgets import *

def download_all_images(urls):
  for url in urls:
    image = ImageData(url)
    image.save_image()
  
  msg_box = QMessageBox()
  msg_box.setIcon(QMessageBox.Icon.Information)
  msg_box.setText("All images have been successfully downloaded.")
  msg_box.setWindowTitle("Download Complete")
  msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
  msg_box.exec()
    

class ImagesWindow(QWidget):
  def __init__(self, url):
    super().__init__()
    if self.parent():
      self.parent().layout().removeWidget(self)

    self.label = QLabel("Here are the images from the website:")
    download_all = QPushButton("Download All")
    download_all.setStyleSheet("background: green; color: white")
    download_all.setCursor(Qt.CursorShape.PointingHandCursor)

    f_widget = QWidget()
    f_layout = QHBoxLayout()
    f_widget.setLayout(f_layout)
    f_layout.addStretch()
    f_layout.addWidget(self.label)
    f_layout.addWidget(download_all)

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
    download_all.clicked.connect(lambda: download_all_images(images_url))

    grid_layout = QGridLayout()
    images_widget.setLayout(grid_layout)
    layout.addWidget(scroll_area)
    row, col = 0, 0

    for url in images_url:
      image_box = QWidget()
      image_box_layout = QVBoxLayout()
      image_box.setLayout(image_box_layout)

      image_label = QLabel()
      image = ImageData(url)
      pixmap = QPixmap()
      pixmap.loadFromData(image.display_image())
      image_label.setPixmap(pixmap)
      image_label.setScaledContents(True)
      image_box_layout.addWidget(image_label)

      button_box = QWidget()
      button_layout = QHBoxLayout()
      button_layout.addStretch()
      button_box.setLayout(button_layout)

      toggle_button = QPushButton("Show Details")
      button_layout.addWidget(toggle_button)
      # image_box_layout.addWidget(toggle_button)

      save_button = QPushButton("Save Image")
      button_layout.addWidget(save_button)
      save_button.setStyleSheet("background: green; color: white")
      # save_button.clicked.connect(lambda url=url: ImageData(url).save_image())
      image_box_layout.addWidget(button_box)

      details_label = QLabel()
      image_properties = image.image_properties()
      details_label.setText(
        f"Image Name: {image_properties['filename']}\n"
        f"Image Size: {image_properties['size']}\n"
        f"Image Format: {image_properties['format']}\n"
        f"File Size: {image_properties['file_size']} MB\n"
      )
      details_label.setVisible(False)
      image_box_layout.addWidget(details_label)

      def save_image_fn(url):
        print(url)
        img = ImageData(url)
        return img.save_image()

      def create_toggle_details_fn(label, button):
        visibility_state = False
        def toggle_details():
          nonlocal visibility_state
          visibility_state = not visibility_state
          label.setVisible(visibility_state)
          button.setText("Hide Details" if visibility_state else "Show Details")
        return toggle_details

      toggle_button.clicked.connect(create_toggle_details_fn(details_label, toggle_button))
      save_button.clicked.connect(lambda url=url: save_image_fn(url))
      
      grid_layout.addWidget(image_box, row, col)
      col += 1
      if col == 5:
        row += 1
        col = 0
