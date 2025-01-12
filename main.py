import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QLabel, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from app.core.settings import Settings
from app.gui.home import HomeWindow
from app.gui.setting import SettingsUI
from app.gui.history import HistoryUI

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Image Downloader")
    self.settings = Settings()

    icon_path = "/home/crowdfrica/Matchoudi/image-downloader/app/gui/assets/logo.png"
    icon = QIcon(icon_path)
    self.setWindowIcon(icon)
    self.tabs = QTabWidget()

    self.tabs.addTab(HomeWindow(self.tabs, self.settings), "Home")
    self.tabs.addTab(AboutWindow(), "About")
    self.tabs.addTab(SettingsUI(self.settings), "Settings")
    self.history_tab = HistoryUI(self.tabs, self.settings)
    self.tabs.addTab(self.history_tab, "History")
    self.tabs.currentChanged.connect(self.__on_tab_change)
    self.setCentralWidget(self.tabs)

  def __on_tab_change(self, index):
    if self.tabs.tabText(index) == "History":
      self.history_tab.thread.start()

# Define the about window
class AboutWindow(QWidget):
  def __init__(self):
    super().__init__()
    description = QLabel(
        "Image Downloader is an open-source application created by Matchoudi Avlessi, a software engineer. "
        "This application allows users to download images from various sources efficiently and manage their download history."
    )
    description.setWordWrap(True)
    description.setStyleSheet("font-size: 18px; font-family: Arial; padding: 100px;")
    description.setAlignment(Qt.AlignmentFlag.AlignCenter)
    description.setFixedHeight(300)
    layout = QVBoxLayout()
    layout.addWidget(description)
    self.setLayout(layout)

# Main entry point
if __name__ == "__main__":
  app = QApplication(sys.argv)
  main_window = MainWindow()
  main_window.show()
  sys.exit(app.exec())
