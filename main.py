import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QLabel, QWidget
from PyQt6.QtGui import QIcon
from app.gui.main_window import HomeWindow
from app.gui.setting import SettingsUI
from app.gui.history import HistoryUI

# Define the main application window with tabs
class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Image Downloader")
    # self.setGeometry(100, 100, 800, 600)

    icon_path = "/home/crowdfrica/Matchoudi/image-downloader/app/gui/assets/logo.png"
    icon = QIcon(icon_path)
    self.setWindowIcon(icon)

    # Create a QTabWidget
    self.tabs = QTabWidget()

    # Create and add tabs
    self.tabs.addTab(HomeWindow(), "Home")
    self.tabs.addTab(AboutWindow(), "About")
    self.tabs.addTab(SettingsUI(), "Settings")
    self.tabs.addTab(HistoryUI(), "History")

    # Set the QTabWidget as the central widget
    self.setCentralWidget(self.tabs)

# Define the about window
class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("This is the About Page!")
        layout.addWidget(label)
        self.setLayout(layout)


# Define the settings window
class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("This is the Settings Page!")
        layout.addWidget(label)
        self.setLayout(layout)


# Main entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
