from PyQt6.QtWidgets import QMessageBox

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