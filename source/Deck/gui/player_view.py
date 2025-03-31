from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
import requests
import os
from dotenv import load_dotenv

class PlayerView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spotify Player")

        load_dotenv()
        self.access_token = os.getenv("SPOTIFY_ACCESS_TOKEN")

        layout = QVBoxLayout()

        self.track_label = QLabel("No song playing")
        layout.addWidget(self.track_label)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_song)
        layout.addWidget(self.play_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_song)
        layout.addWidget(self.pause_button)

        self.setLayout(layout)

        self.update_song_info()

    def update_song_info(self):
        """Fetches the currently playing song"""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            track_name = data["item"]["name"]
            artist_name = data["item"]["artists"][0]["name"]
            self.track_label.setText(f"Now Playing: {track_name} - {artist_name}")

    def play_song(self):
        """Send play request to Spotify"""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        requests.put("https://api.spotify.com/v1/me/player/play", headers=headers)

    def pause_song(self):
        """Send pause request to Spotify"""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        requests.put("https://api.spotify.com/v1/me/player/pause", headers=headers)
