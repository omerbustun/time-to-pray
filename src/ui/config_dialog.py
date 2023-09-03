from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt6.QtGui import QIcon
from api.fetch_times import read_config, write_config, validate_location, METHODS
import os

ICON_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "icon.png")

class ConfigDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set the window title
        self.setWindowTitle("Time to Pray - Settings")

        # Set the window icon
        self.setWindowIcon(QIcon(ICON_PATH))

        self.city_input = QLineEdit(self)
        self.country_input = QLineEdit(self)
        
        # Read-only fields for Latitude and Longitude
        self.lat_label = QLabel("Latitude: N/A")
        self.lon_label = QLabel("Longitude: N/A")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("City:"))
        layout.addWidget(self.city_input)
        layout.addWidget(QLabel("Country:"))
        layout.addWidget(self.country_input)
        layout.addWidget(self.lat_label)
        layout.addWidget(self.lon_label)

        self.method_dropdown = QComboBox(self)
        self.method_dropdown.addItems(METHODS.keys())
        layout.addWidget(QLabel("Method:"))
        layout.addWidget(self.method_dropdown)

        # Adding a label to show the "Saved!" message
        self.saved_label = QLabel("")
        layout.addWidget(self.saved_label)
        
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_config)
        layout.addWidget(save_button)

        self.load_existing_settings()
        
    def load_existing_settings(self):
        config = read_config()
        if "city" in config:
            self.city_input.setText(config["city"])
        if "country" in config:
            self.country_input.setText(config["country"])
        if "latitude" in config:
            self.lat_label.setText(f"Latitude: {config['latitude']}")
        else:
            self.lat_label.setText(f"Latitude: N/A")
        if "longitude" in config:
            self.lon_label.setText(f"Longitude: {config['longitude']}")
        else:
            self.lat_label.setText(f"Longitude: N/A")
        if "method" in config:
            # Find the method name using the method id
            method_name = [name for name, id in METHODS.items() if id == config["method"]][0]

            # Set the current index of the dropdown to the index of the method name
            index = self.method_dropdown.findText(method_name)
            if index != -1:  # Ensure the method name was found in the dropdown
                self.method_dropdown.setCurrentIndex(index)


    def save_config(self):
        city = self.city_input.text()
        country = self.country_input.text()

        # Fetch the selected method's ID from the dropdown
        method_name = self.method_dropdown.currentText()
        method_id = METHODS[method_name]  # This will get the ID using the method name as the key

        latitude, longitude = validate_location(city, country, method=str(method_id))
        if latitude and longitude:
            self.lat_label.setText(f"Latitude: {latitude}")
            self.lon_label.setText(f"Longitude: {longitude}")

            # Save the city, country, latitude, longitude, and method ID to the config
            write_config({
                "city": city,
                "country": country,
                "latitude": latitude,
                "longitude": longitude,
                "method": method_id
            })

            self.saved_label.setText("Saved!")
        else:
            self.saved_label.setText("Invalid city or country. Please check your input.")

    



