import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from ..core.website_content import Content
from ..core.image import ImageData

from PyQt6.QtWidgets import *

class ImagesWindow(QWidget):
  def __init__(self, url):
    super().__init__()
    self.label = QLabel("Here are the images from the website:")

    layout = QVBoxLayout()
    layout.addStretch()
    self.setLayout(layout)
    layout.addWidget(self.label)

    scroll_area = QScrollArea()
    scroll_area.setMinimumHeight(500)
    scroll_area.setWidgetResizable(True)

    images_widget = QWidget()
    scroll_area.setWidget(images_widget)

    # images = ['image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8', 'image9', 'image10']
    web_content = Content(url)
    images_url = web_content.get_images()
    # print(images_url)
    row, col = 0, 0

    grid_layout = QGridLayout()
    images_widget.setLayout(grid_layout)
    layout.addWidget(scroll_area)
    for url in images_url:
      # print(type(url))
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

      toggle_button = QPushButton("Show Details")
      image_box_layout.addWidget(toggle_button)

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

      def create_toggle_details_fn(label, button):
        visibility_state = False
        def toggle_details():
          nonlocal visibility_state
          visibility_state = not visibility_state
          label.setVisible(visibility_state)
          button.setText("Hide Details" if visibility_state else "Show Details")
        return toggle_details

      toggle_button.clicked.connect(create_toggle_details_fn(details_label, toggle_button))
      
      grid_layout.addWidget(image_box, row, col)
      col += 1
      if col == 5:
        row += 1
        col = 0

    