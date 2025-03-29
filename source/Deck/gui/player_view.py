from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QTimer

class PlayerView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Spotify Player")
        self.setGeometry(100, 100, 400, 200)

        # Layout
        self.layout = QVBoxLayout()

        # Label to show current status
        self.song_label = QLabel("No song is playing", self)
        self.layout.addWidget(self.song_label)

        # Add a button to refresh the song info
        self.refresh_button = QPushButton("Refresh Song", self)
        self.refresh_button.clicked.connect(self.update_song)
        self.layout.addWidget(self.refresh_button)

        # Set layout
        self.setLayout(self.layout)

        # Initially update the song info
        self.update_song()

    def update_song(self):
        """Update the song information after the user logs in"""
        #track_name, artist_name = get_current_track()

        #if track_name:
        #    self.song_label.setText(f"Now Playing: {track_name} by {artist_name}")
        #else:
        #    self.song_label.setText("No song is currently playing")
        pass
