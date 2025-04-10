from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import QTimer, pyqtSignal, Qt
from PyQt6.QtGui import QFont
import requests
import webbrowser

class LoginView(QWidget):
    login_successful = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spotify Login")
        
        layout = QVBoxLayout()

        self.label = QLabel("Please log in to Spotify.",
                            alignment=Qt.AlignmentFlag.AlignCenter,
                            font=QFont("Segoe UI Variable", 15, weight=QFont.Weight.Bold))
        self.label.setStyleSheet("color: black;")
        layout.addWidget(self.label)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.start_login)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: lightgray;
                color: black;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI Variable';
                font-size: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: darkgray;
            }
            QPushButton:pressed {
                background-color: gray;
            }
        """)
        layout.addWidget(self.login_button)

        self.setLayout(layout)
        
        # Create a timer to check for login status
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_login_status)

    def start_login(self):
        """Opens Spotify login page and starts polling for token"""
        webbrowser.open("http://127.0.0.1:8888/login")
        self.label.setText("Waiting for authentication...")

        # Start polling Flask server every 2 seconds
        self.timer.start(2000)

    def check_login_status(self):
        """Checks Flask server to see if user is logged in"""
        try:
            response = requests.get("http://localhost:8888/token_status")
            if response.json().get("logged_in"):
                self.timer.stop()  # Stop polling
                self.login_successful.emit()  # Switch to player UI
        except requests.exceptions.RequestException:
            pass  # Ignore errors if server is not ready yet
