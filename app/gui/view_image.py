from PyQt6.QtWidgets import (
  QVBoxLayout,
  QHBoxLayout,
  QSlider,
  QLabel,
  QPushButton,
  QFileDialog,
  QWidget,
  QSpinBox,
  QScrollArea
)
from PyQt6.QtCore import Qt
from PIL import Image, ImageEnhance
from PIL.ImageQt import ImageQt
from PyQt6.QtGui import QPixmap

class ViewImageUI(QWidget):
  def __init__(self, imageWidget, tabs):
    super().__init__()
    self.original_image = imageWidget.image
    self.output_path = imageWidget.file_output_path
    self.current_image = self.original_image
    self.layout = QVBoxLayout(self)
    self.tabs = tabs

    self.scroll_area = QScrollArea()
    self.image_label = QLabel()
    self.scroll_area.setWidget(self.image_label)
    self.scroll_area.setWidgetResizable(True)
    self.scroll_area.setFixedHeight(400)
    self.layout.addWidget(self.scroll_area)
    self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.display_image()
    # self.layout.addWidget(self.image_label)

    self.aspect_ratio = self.original_image.width / self.original_image.height

    # Sliders
    self.brightness_slider = self.create_slider("Brightness")
    self.contrast_slider = self.create_slider("Contrast")
    self.sharpness_slider = self.create_slider("Sharpness")

    self.tabs.addTab(self, "Image")
    self.tabs.setCurrentWidget(self)
    
    # Crop Layout
    crop_widget = QWidget()
    crop_layout = QHBoxLayout(crop_widget)
    crop_widget.setFixedWidth(300)
    self.x_spinbox = self.create_spinbox("X", crop_layout)
    self.x_spinbox.editingFinished.connect(self.update_height)
    self.y_spinbox = self.create_spinbox("Y", crop_layout)
    self.y_spinbox.editingFinished.connect(self.update_width)

    self.resize_button = QPushButton("Resize")
    self.resize_button.clicked.connect(self.resize_image)
    self.resize_button.setStyleSheet("""
      QPushButton {
      background: green; 
      color: white; 
      padding: 5px;
      }
      QPushButton:hover {
      background: darkgreen;
      }
    """)
    self.resize_button.setFixedWidth(80)
    crop_layout.addWidget(self.resize_button)
    self.layout.addWidget(crop_widget)
    
    button_widget = QWidget()
    button_layout = QHBoxLayout(button_widget)
    button_layout.addStretch()
    
    self.save_button = QPushButton("Save Image")
    self.save_button.clicked.connect(self.save_image)
    self.save_button.setStyleSheet("""
      QPushButton {
      background: green; 
      color: white; 
      padding: 8px;
      }
      QPushButton:hover {
      background: darkgreen;
      }
    """)
    button_layout.addWidget(self.save_button)

    self.reset_button = QPushButton("Reset")
    self.reset_button.clicked.connect(lambda: self.reset_image(imageWidget))
    self.reset_button.setStyleSheet("""
      QPushButton {
        border: 1px solid red;
        color: white;
        padding: 8px
      }
      QPushButton:hover {
        background: red;
      }
    """)
    button_layout.addWidget(self.reset_button)
    self.layout.addWidget(button_widget)

    close_btn = QPushButton("<-- Close")
    close_btn.clicked.connect(self.close_existing_tab)
    close_btn.setStyleSheet("background: red; color: white; padding: 10px")
    close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
    self.layout.addWidget(close_btn)

  def create_slider(self, label_text):
    """Helper to create a slider with a label."""
    label = QLabel(label_text)
    self.layout.addWidget(label)

    slider = QSlider(Qt.Orientation.Horizontal)
    slider.setRange(0, 200)
    slider.setValue(100)
    slider.valueChanged.connect(self.update_image)
    self.layout.addWidget(slider)
    return slider
  
  def reset_sliders(self):
    self.brightness_slider.setValue(100)
    self.contrast_slider.setValue(100)
    self.sharpness_slider.setValue(100)
  
  def update_image(self):
    """Update the image based on slider values."""
    if not self.original_image:
      return

    brightness_factor = self.brightness_slider.value() / 100  # Scale to 0.0 - 2.0
    contrast_factor = self.contrast_slider.value() / 100
    sharpness_factor = self.sharpness_slider.value() / 100

    image = self.original_image
    image = ImageEnhance.Brightness(image).enhance(brightness_factor)
    image = ImageEnhance.Contrast(image).enhance(contrast_factor)
    image = ImageEnhance.Sharpness(image).enhance(sharpness_factor)

    self.current_image = image
    self.display_image()

  def save_image(self):
    """Save the adjusted image with good quality."""
    if self.current_image:
      file_path, _ = QFileDialog.getSaveFileName(
        self,
        "Save Image",
        self.output_path,
        "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
      )
      if file_path:
        file_extension = file_path.split('.')[-1].lower()

        try:
          if file_extension in ["jpg", "jpeg"]:
            self.current_image.save(file_path, format="JPEG", quality=95, optimize=True, progressive=True)
          elif file_extension == "png":
            self.current_image.save(file_path, format="PNG", optimize=True)
          else:
            self.current_image.save(file_path)
          print(f"Image saved successfully to {file_path}")
        except Exception as e:
          print(f"Error saving image: {e}")

  def display_image(self):
    """Display the current image in the QLabel."""
    qt_image = ImageQt(self.current_image)
    pixmap = QPixmap.fromImage(qt_image)
    width = self.current_image.width
    height = self.current_image.height
    self.image_label.setPixmap(pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
    # self.image_label.setScaledContents(True)

  def update_width(self):
    """Update the Width of the image."""
    new_height = self.y_spinbox.value()
    new_width = int(new_height * self.aspect_ratio)
    self.x_spinbox.setValue(new_width)

  def update_height(self):
    """Update the height of the image"""
    new_width = self.x_spinbox.value()
    new_height = int(new_width / self.aspect_ratio)
    self.y_spinbox.setValue(new_height)

  def create_spinbox(self, label_text, layout):
    """Helper to create a spinbox with a label."""
    label = QLabel(label_text)
    label.setFixedWidth(20)
    layout.addWidget(label)

    spinbox = QSpinBox()
    spinbox.setRange(1, 5000)
    if label_text == "X":
      spinbox.setValue(self.original_image.width)
    else:
      spinbox.setValue(self.original_image.height)

    layout.addWidget(spinbox)
    return spinbox
  
  def resize_image(self):
    """Resize the image based on user input."""
    if not self.original_image:
      return

    new_width = self.x_spinbox.value()
    new_height = self.y_spinbox.value()

    # Resize the image
    self.current_image = self.current_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    self.original_image = self.current_image
    self.display_image()
    self.reset_sliders()

  def reset_image(self, image_widget):
    """Reset the image to the original state."""
    self.original_image = image_widget.image
    self.current_image = self.original_image
    self.reset_sliders()
    self.display_image()

  def close_existing_tab(self):
    for i in range(self.tabs.count()):
      if self.tabs.tabText(i) == "Image":
        self.tabs.removeTab(i)
        break