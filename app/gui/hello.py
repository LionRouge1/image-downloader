# import sys
# from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QPushButton
import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

# app = QApplication([])

# window = QWidget()
# window.setWindowTitle("Hello Window")
# window.setGeometry(100, 100, 280, 80)
# helloMsg = QLabel("Hello, World!", parent=window)
# helloMsg.move(60, 15)

# window.show()
# sys.exit(app.exec())

# def main():
#    # Create the application instance
#    app = QApplication(sys.argv)

#    # Create the main window
#    window = QMainWindow()
#    window.setWindowTitle("Simple PyQt Example")
#    window.setGeometry(100, 100, 400, 200)

#    # Create a label widget
#    label = QLabel("Hello, PyQt!", window)
#    label.move(150, 80)

#    # Show the window
#    window.show()

#    # Execute the application
#    sys.exit(app.exec())

# if __name__ == "__main__":
#    main()

def window():
   app = QApplication(sys.argv)
   win = QDialog()
   b1 = QPushButton(win)
   b1.setText("Button1")
   b1.move(50,20)
   b1.clicked.connect(b1_clicked)

   b2 = QPushButton(win)
   b2.setText("Button2")
   b2.move(50,50)
   b2.clicked.connect(b2_clicked)
  #  QObject.connect(b2,SIGNAL("clicked()"),b2_clicked)

   win.setGeometry(100,100,200,100)
   win.setWindowTitle("PyQt")
   win.show()
   sys.exit(app.exec())

def b1_clicked():
   print("Button 1 clicked")

def b2_clicked():
   print("Button 2 clicked")

if __name__ == '__main__':
   window()