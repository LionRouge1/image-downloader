# import tkinter as tk

# # Create the main window
# root = tk.Tk()
# root.title("Hello Window")

# # Create a label widget with the text "Hello, World!"
# label = tk.Label(root, text="Hello, World!", font=("Helvetica", 16))

# # Place the label in the window
# label.pack(pady=20)

# # Run the Tkinter event loop
# root.mainloop()

# import sys
# from PyQt6.QtGui import QAction
# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QMenuBar, QVBoxLayout, QLabel, QWidget
# )


# # Define the main application window
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Navigation Bar Example")

#         # Create a menu bar
#         menu_bar = self.menuBar()

#         # Add menus and actions
#         file_menu = menu_bar.addMenu("File")
#         home_action = QAction("Home", self)
#         about_action = QAction("About", self)
#         settings_action = QAction("Settings", self)

#         file_menu.addAction(home_action)
#         file_menu.addAction(about_action)
#         file_menu.addAction(settings_action)

#         # Connect menu actions to methods
#         home_action.triggered.connect(self.open_home)
#         about_action.triggered.connect(self.open_about)
#         settings_action.triggered.connect(self.open_settings)

#         # Set initial central widget
#         self.home_window = HomeWindow()
#         self.setCentralWidget(self.home_window)

#     def open_home(self):
#         self.home_window = HomeWindow()
#         self.setCentralWidget(self.home_window)

#     def open_about(self):
#         self.about_window = AboutWindow()
#         self.setCentralWidget(self.about_window)

#     def open_settings(self):
#         self.settings_window = SettingsWindow()
#         self.setCentralWidget(self.settings_window)


# # Define the home window
# class HomeWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout()
#         label = QLabel("Welcome to the Home Page!")
#         layout.addWidget(label)
#         self.setLayout(layout)


# # Define the about window
# class AboutWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout()
#         label = QLabel("This is the About Page!")
#         layout.addWidget(label)
#         self.setLayout(layout)


# # Define the settings window
# class SettingsWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout()
#         label = QLabel("This is the Settings Page!")
#         layout.addWidget(label)
#         self.setLayout(layout)


# # Main entry point
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_window = MainWindow()
#     main_window.show()
#     sys.exit(app.exec())




import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QLabel, QWidget


# Define the main application window with tabs
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navigation Tabs Example")
        self.setGeometry(100, 100, 800, 600)

        # Create a QTabWidget
        self.tabs = QTabWidget()

        # Create and add tabs
        self.tabs.addTab(HomeWindow(), "Home")
        self.tabs.addTab(AboutWindow(), "About")
        self.tabs.addTab(SettingsWindow(), "Settings")

        # Set the QTabWidget as the central widget
        self.setCentralWidget(self.tabs)


# Define the home window
class HomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Welcome to the Home Page!")
        layout.addWidget(label)
        self.setLayout(layout)


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
