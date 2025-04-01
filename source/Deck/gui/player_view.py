from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QTimer
import requests
import os
from dotenv import load_dotenv
from spotify_api import SpotifyAPI

class PlayerView(QWidget):
    def __init__(self):
        super().__init__()
        
        self.sp = SpotifyAPI()
        
        self.setWindowTitle("Spotify Player")

        load_dotenv()
        self.access_token = os.getenv("ACCESS_TOKEN")

        layout = QVBoxLayout()

        self.track_label = QLabel("No song playing")
        layout.addWidget(self.track_label)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.sp.play)
        layout.addWidget(self.play_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.sp.pause)
        layout.addWidget(self.pause_button)

        self.setLayout(layout)

        # Configure Timer and Start
        self.song_timer = QTimer(self)
        self.song_timer.timeout.connect(self.update_song_info)
        self.song_timer.start(1000)
        
        # Configure Refresh Token Timer
        self.token_timer = QTimer(self)
        self.token_timer.timeout.connect(self.sp.refresh_token)
        self.token_timer.start(300000)  # 5 minutes

    def update_song_info(self):
        artist_name, track_name, album_cover = self.sp.get_current_song()
        print(album_cover)
        self.track_label.setText(f"{track_name} - {artist_name}")

