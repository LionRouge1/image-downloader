import sys
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QWidget

class Spinner(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.angle = 0

    # Set up a timer to update the spinner
    self.timer = QTimer()
    self.timer.timeout.connect(self.update_spinner)
    self.timer.start(50)  # 50 ms interval

  def update_spinner(self):
    self.angle += 10
    if self.angle >= 360:
      self.angle = 0
    self.update()  # Trigger a repaint

  def paintEvent(self, event):
    with QPainter(self) as painter:
      painter.setRenderHint(QPainter.RenderHint.Antialiasing)

      # Draw the spinner
      pen = QPen()
      pen.setWidth(5)
      pen.setColor(Qt.GlobalColor.darkYellow)
      pen.setCapStyle(Qt.PenCapStyle.RoundCap)
      painter.setPen(pen)
      painter.translate(self.width() // 2, self.height() // 2)
      painter.rotate(self.angle)

      painter.drawLine(0, 0, 15, 0)
