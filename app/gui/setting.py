import sys

from PyQt6.QtWidgets import (
  QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QFileDialog
)

class SettingsUI(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()

  def initUI(self):
    layout = QVBoxLayout()

    # Directory selection
    self.dir_label = QLabel('Select Directory to Save Images:')
    layout.addWidget(self.dir_label)

    self.dir_line_edit = QLineEdit(self)
    layout.addWidget(self.dir_line_edit)

    self.dir_button = QPushButton('Browse', self)
    self.dir_button.clicked.connect(self.select_directory)
    layout.addWidget(self.dir_button)

    # Enable CSS images
    self.css_checkbox = QCheckBox('Enable CSS Images', self)
    layout.addWidget(self.css_checkbox)

    # Save button
    self.save_button = QPushButton('Save Settings', self)
    layout.addWidget(self.save_button)

    self.setLayout(layout)
    self.setWindowTitle('Settings')

  def select_directory(self):
    directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
    if directory:
      self.dir_line_edit.setText(directory)

if __name__ == '__main__':
  app = QApplication(sys.argv)
  settings_ui = SettingsUI()
  settings_ui.show()
  sys.exit(app.exec())