from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QScrollArea, QPushButton
from .image import ImageWidget

class ViewHistoryUI(QWidget):
  def __init__(self, tab_widget, history, callback):
    super().__init__()
    self.tab_widget = tab_widget
    self.close_existing_tab()
    callback(history['id'])
    
    self.images = []
    self.tab_widget.addTab(self, "View History")
    self.tab_widget.setCurrentWidget(self)
    self.main_layout = QVBoxLayout(self)

    close_btn = QPushButton("Close")
    close_btn.clicked.connect(self.close_existing_tab)
    close_btn.setStyleSheet("background: red; color: white; padding: 10px")
    self.main_layout.addWidget(close_btn)
    
    scroll_area = QScrollArea()
    scroll_area.setMinimumHeight(500)
    scroll_area.setWidgetResizable(True)

    self.images_widget = QWidget()
    scroll_area.setWidget(self.images_widget)

    self.grid_layout = QGridLayout()
    self.images_widget.setLayout(self.grid_layout)
    self.main_layout.addWidget(scroll_area)

    if history['images']:
      for index, image in enumerate(history['images']):
        image_widget = ImageWidget(image, self)
        self.grid_layout.addWidget(image_widget, index // 4, index % 4)
    else:
      label = QLabel("No image")
      self.grid_layout.addWidget(label, 0, 0)

  def close_existing_tab(self):
        # Find and remove the "Cities" tab
    for i in range(self.tab_widget.count()):
      if self.tab_widget.tabText(i) == "View History":
        self.tab_widget.removeTab(i)
        break
