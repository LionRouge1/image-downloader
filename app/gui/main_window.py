import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator, QFont

def window():
    app = QApplication(sys.argv)
    win = QWidget()

    label = QLabel("Enter Website URL:")
    url_input = QLineEdit()
    url_regex = QRegularExpression(r"^(https?|ftp)://[^\s/$.?#].[^\s]*$")
    validator = QRegularExpressionValidator(url_regex, url_input)
    url_input.setValidator(validator)
    url_input.setPlaceholderText("https://www.example.com")
    url_input.setStyleSheet("height: 20px; padding: 10px")
    url_input.setMaximumWidth(400)

    search_btn = QPushButton("Search")
    search_btn.setStyleSheet("height: 20px; padding: 10px")


    search_box = QHBoxLayout()
    search_box.addWidget(label)
    search_box.addWidget(url_input)
    search_box.addWidget(search_btn)

    search_box_container = QWidget()
    search_box_container.setLayout(search_box)
    search_box_container.setMaximumWidth(600) 

    center_layout = QHBoxLayout()
    center_layout.addStretch()
    center_layout.addWidget(search_box_container)
    center_layout.addStretch()
    
    main_layout = QVBoxLayout()
    main_layout.addWidget(search_box_container)
    main_layout.addStretch()
    win.setLayout(main_layout)

    win.setStyleSheet("font-size: 16px; font-family: Arial;")
    win.setMinimumWidth(700)
    win.setWindowTitle("Images Downloader")
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    window()