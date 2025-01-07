import sys
from PyQt6.QtGui import QIntValidator

from PyQt6.QtWidgets import (
  QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QFileDialog, QGridLayout
)
from ..core.setting import save_settings, load_settings

class SettingsUI(QWidget):
  def __init__(self):
    super().__init__()
    self.settings = load_settings()
    layout = QVBoxLayout()
    # layout.addStretch()
    self.setLayout(layout)
    self.params_widget = QWidget()
    params_layout = QGridLayout()
    params_layout.setSpacing(10)
    self.params_widget.setLayout(params_layout)

    # Directory selection
    self.dir_label = QLabel('Select Directory to Save Images:')
    params_layout.addWidget(self.dir_label, 0, 0)

    self.dir_line_edit = QLineEdit(self)
    params_layout.addWidget(self.dir_line_edit, 0, 1)
    self.dir_line_edit.setText(self.settings['save_directory'])
    self.dir_line_edit.setReadOnly(True)

    self.dir_button = QPushButton('Browse', self)
    self.dir_button.clicked.connect(self.select_directory)
    params_layout.addWidget(self.dir_button, 0, 2)


    # Max images
    self.max_image_label = QLabel("Max Images per request:")
    params_layout.addWidget(self.max_image_label, 1, 0)

    self.max_image_line_edit = QLineEdit(self)
    self.max_image_line_edit.setValidator(QIntValidator(2, 999, self))
    self.max_image_line_edit.setText(str(self.settings['max_images']))
    self.max_image_line_edit.textChanged.connect(self.save_setting)
    params_layout.addWidget(self.max_image_line_edit, 1, 1)

    self.max_image_description_label = QLabel('Specify the maximum number of images to download per request.')
    self.max_image_description_label.setWordWrap(True)
    self.max_image_description_label.setStyleSheet('''
      color: grey;
      font-size: 12px;
    ''')
    params_layout.addWidget(self.max_image_description_label, 2, 1)

    # Enable CSS images
    self.enable_css_images_label = QLabel('Enable CSS Images:')
    self.enable_css_images_label.mousePressEvent = lambda event: self.css_checkbox.toggle()
    params_layout.addWidget(self.enable_css_images_label, 3, 0)
    
    self.css_checkbox = QCheckBox(self)
    self.css_checkbox.setChecked(self.settings['get_css_images'])
    self.css_checkbox.setStyleSheet('''
      QCheckBox::indicator {
      width: 15px;
      height: 15px;
      };
    ''')
    self.css_checkbox.stateChanged.connect(self.save_setting)
    params_layout.addWidget(self.css_checkbox, 3, 1)

    # Description for CSS images checkbox
    self.css_description_label = QLabel('When checked, CSS images will be downloaded along with the main images.')
    self.css_description_label.setWordWrap(True)
    self.css_description_label.setStyleSheet('''
      color: grey;
      font-size: 12px;
    ''')
    params_layout.addWidget(self.css_description_label, 4, 1)

    # Save button
    self.save_button = QPushButton('Save Settings', self)
    self.save_button.clicked.connect(self.save_setting)
    layout.addWidget(self.params_widget)
    layout.addWidget(self.save_button)

    self.setWindowTitle('Settings')

  def select_directory(self):
    directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
    if directory:
      self.dir_line_edit.setText(directory)
      self.save_setting()

  def save_setting(self):
    directory = self.dir_line_edit.text()
    max = self.max_image_line_edit.text()
    get_css = self.css_checkbox.isChecked()

    save_settings(directory, max, get_css)

if __name__ == '__main__':
  app = QApplication(sys.argv)
  settings_ui = SettingsUI()
  settings_ui.show()
  sys.exit(app.exec())