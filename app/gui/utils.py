from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

def show_success_message(message):
  msg_box = QMessageBox()
  msg_box.setIcon(QMessageBox.Icon.Information)
  msg_box.setText("Success")
  msg_box.setInformativeText(message)
  msg_box.setWindowTitle("Success")
  msg_box.exec()

def show_error_message(message):
  msg_box = QMessageBox()
  msg_box.setIcon(QMessageBox.Icon.Critical)
  msg_box.setText("Error")
  msg_box.setInformativeText(message)
  msg_box.setWindowTitle("Error")
  msg_box.exec()

class CustomErrorDialog(QDialog):
  def __init__(self, message, parent=None):
    super().__init__(parent)
    self.setWindowTitle("Error")
    self.setFixedSize(300, 150)
      
    layout = QVBoxLayout(self)
      
    self.label = QLabel(message)
    layout.addWidget(self.label)
      
    self.close_button = QPushButton("Close")
    self.close_button.clicked.connect(self.close)
    layout.addWidget(self.close_button)

def show_custom_error_message(message):
  dialog = CustomErrorDialog(message)
  dialog.exec()