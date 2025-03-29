from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget

class LoginView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        # Status Label
        self.status_label = QLabel("Please log in to Spotify.", self)
        self.layout.addWidget(self.status_label)

        # Button to invoke login
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        # Set Layout
        self.setLayout(self.layout)

    def login(self):
        self.status_label.setText("Redirecting to spotify...")

        

        self.status_label.setText("Awaiting for authorization code...")

    