from PyQt6.QtWidgets import (
    QApplication, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QPushButton, QFileDialog, QWidget
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class GraphicsViewExample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QGraphicsView Example")
        self.resize(800, 600)

        # Layout
        self.layout = QVBoxLayout()

        # QGraphicsView and QGraphicsScene
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        self.layout.addWidget(self.graphics_view)

        # Button to load an image
        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)
        self.layout.addWidget(self.load_button)

        self.setLayout(self.layout)

    def load_image(self):
        # Open a file dialog to select an image
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_path:
            # Create a QPixmap from the image file
            pixmap = QPixmap(file_path)

            # Add the pixmap to the QGraphicsScene
            self.scene.clear()  # Clear previous items
            self.pixmap_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.pixmap_item)

            # Fit the view to the image
            self.graphics_view.fitInView(self.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)


if __name__ == "__main__":
    app = QApplication([])
    window = GraphicsViewExample()
    window.show()
    app.exec()
