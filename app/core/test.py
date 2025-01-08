import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QLabel, QMainWindow, QWidget, QTabWidget

# Data: Countries and their cities
data = {
    "USA": ["New York", "Los Angeles", "Chicago"],
    "Canada": ["Toronto", "Vancouver", "Montreal"],
    "UK": ["London", "Manchester", "Birmingham"]
}

# Main Application Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Countries and Cities")

        # Tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Countries tab
        self.countries_tab = QWidget()
        self.tab_widget.addTab(self.countries_tab, "Countries")

        # Layout for the countries tab
        self.countries_layout = QVBoxLayout()
        self.countries_tab.setLayout(self.countries_layout)

        # Add buttons for each country
        for country, cities in data.items():
            button = QPushButton(f"View cities in {country}")
            button.clicked.connect(lambda _, c=country, ci=cities: self.add_cities_tab(c, ci))
            self.countries_layout.addWidget(button)

    def add_cities_tab(self, country, cities):
        # Check if a cities tab already exists
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == "Cities":
                self.tab_widget.removeTab(i)
                break

        # Create a new cities tab
        self.cities_tab = QWidget()
        self.tab_widget.addTab(self.cities_tab, "Cities")

        # Layout for the cities tab
        self.cities_layout = QVBoxLayout()
        self.cities_tab.setLayout(self.cities_layout)

        # Add the title
        self.cities_layout.addWidget(QLabel(f"Cities in {country}:"))

        # Add the list of cities
        for city in cities:
            self.cities_layout.addWidget(QLabel(city))

        # Add a "Close Tab" button
        close_button = QPushButton("Close Tab")
        close_button.clicked.connect(self.close_cities_tab)
        self.cities_layout.addWidget(close_button)

        # Switch to the cities tab
        self.tab_widget.setCurrentWidget(self.cities_tab)

    def close_cities_tab(self):
        # Find and remove the "Cities" tab
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == "Cities":
                self.tab_widget.removeTab(i)
                break

# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
