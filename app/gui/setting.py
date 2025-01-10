from PyQt6.QtGui import QIntValidator

from PyQt6.QtWidgets import (
  QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QFileDialog, QGridLayout, QGroupBox
)
# from ..core.settings import save_settings, load_settings

class SettingsUI(QWidget):
  def __init__(self, settings):
    super().__init__()
    self.settings = settings
    layout = QVBoxLayout(self)
    self.setFixedHeight(500)
    params_layout = QGridLayout()

    group_box = QGroupBox("Settings")
    group_box.setFixedSize(600, 400)
    group_box.setLayout(params_layout)

    # Directory selection
    self.dir_label = QLabel('Select Directory to Save Images:')
    self.dir_label.setStyleSheet("font-size: 16px; font-family: Arial;")
    params_layout.addWidget(self.dir_label, 0, 0)

    self.dir_line_edit = QLineEdit(self)
    self.dir_line_edit.setStyleSheet("padding: 5px 10px")
    params_layout.addWidget(self.dir_line_edit, 0, 1)
    self.dir_line_edit.setText(self.settings.save_directory)
    self.dir_line_edit.setReadOnly(True)

    self.dir_button = QPushButton('Browse', self)
    self.dir_button.setStyleSheet("background: green; color: white; padding: 5px 10px")
    self.dir_button.clicked.connect(self.select_directory)
    params_layout.addWidget(self.dir_button, 0, 2)

    # Max images
    self.max_image_label = QLabel("Max Images per request:")
    self.max_image_label.setStyleSheet("font-size: 16px; font-family: Arial;")
    params_layout.addWidget(self.max_image_label, 1, 0)

    self.max_image_line_edit = QLineEdit(self)
    self.max_image_line_edit.setStyleSheet("padding: 5px 10px")
    self.max_image_line_edit.setValidator(QIntValidator(2, 999, self))
    self.max_image_line_edit.setText(str(self.settings.max_images))
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
    self.enable_css_images_label.setStyleSheet("font-size: 16px; font-family: Arial;")
    self.enable_css_images_label.mousePressEvent = lambda event: self.css_checkbox.toggle()
    params_layout.addWidget(self.enable_css_images_label, 3, 0)
    
    self.css_checkbox = QCheckBox(self)
    self.css_checkbox.setChecked(self.settings.get_css_images)
    self.css_checkbox.setStyleSheet('''
      QCheckBox::indicator {
      width: 15px;
      height: 15px;
      padding: 5px
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

    # simulate browser for websites that use JS to load images
    self.simulate_browser_label = QLabel('Simulate Browser:')
    self.simulate_browser_label.setStyleSheet("font-size: 16px; font-family: Arial;")
    self.simulate_browser_label.mousePressEvent = lambda event: self.browser_checkbox.toggle()
    params_layout.addWidget(self.simulate_browser_label, 5, 0)

    self.browser_checkbox = QCheckBox(self)
    self.browser_checkbox.setChecked(self.settings.simulate)
    self.browser_checkbox.setStyleSheet('''
      QCheckBox::indicator {
      width: 15px;
      height: 15px;
      padding: 5px
      };
    ''')
    self.browser_checkbox.stateChanged.connect(self.save_setting)
    params_layout.addWidget(self.browser_checkbox, 5, 1)

    # Description for simulate browser checkbox
    self.browser_description_label = QLabel('When checked, the application will simulate a browser to load images. This is useful for websites that use JavaScript to load content, such as those built with React, Next.js...')
    self.browser_description_label.setWordWrap(True)
    self.browser_description_label.setStyleSheet('''
      color: grey;
      font-size: 12px;
    ''')
    params_layout.addWidget(self.browser_description_label, 6, 1)

    # Show browser when stimulating
    self.show_browser_label = QLabel('Show Browser:')
    self.show_browser_label.setDisabled(not self.settings.simulate)
    self.show_browser_label.setStyleSheet("font-size: 16px; font-family: Arial;")
    self.show_browser_label.mousePressEvent = lambda event: self.show_browser_checkbox.toggle()
    params_layout.addWidget(self.show_browser_label, 7, 0)

    self.show_browser_checkbox = QCheckBox(self)
    self.show_browser_checkbox.setDisabled(not self.settings.simulate)
    self.show_browser_checkbox.setChecked(self.settings.show_browser)
    self.show_browser_checkbox.setStyleSheet('''
      QCheckBox::indicator {
      width: 15px;
      height: 15px;
      padding: 5px
      };
    ''')
    self.show_browser_checkbox.stateChanged.connect(self.save_setting)
    params_layout.addWidget(self.show_browser_checkbox, 7, 1)

    # Description for show browser checkbox
    self.show_browser_description_label = QLabel('When checked, the browser will be displayed during simulation. This is useful for websites that block requests from headless browsers.')
    self.show_browser_description_label.setWordWrap(True)
    self.show_browser_description_label.setStyleSheet('''
      color: grey;
      font-size: 12px;
    ''')
    params_layout.addWidget(self.show_browser_description_label, 8, 1)

    # Save button
    self.save_button = QPushButton('Save Settings', self)
    self.save_button.setFixedSize(120, 40)
    self.save_button.setStyleSheet("background: green; color: white; padding: 10px")
    self.save_button.clicked.connect(self.save_setting)
    layout.addWidget(group_box)
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
    simulate = self.browser_checkbox.isChecked()
    show_browser = self.show_browser_checkbox.isChecked()
    self.show_browser_checkbox.setDisabled(not simulate)
    self.show_browser_label.setDisabled(not simulate)

    self.settings.save_settings(directory, max, get_css, simulate, show_browser)
