from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton 
from PyQt6.QtCore import QTimer, Qt, QSize
from PyQt6.QtGui import QFont
import requests
import os
from dotenv import load_dotenv
from spotify_api import SpotifyAPI

class PlayerView(QWidget):
    def __init__(self):
        super().__init__()
        
        self.sp = SpotifyAPI()
        
        self.setWindowTitle("Spotify Player")
        self.setFixedSize(QSize(320,460))

        load_dotenv()
        self.access_token = os.getenv("ACCESS_TOKEN")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.album_cover = QLabel()
        layout.addWidget(self.album_cover,
                         alignment=Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel("No song playing",
                            alignment=Qt.AlignmentFlag.AlignCenter,
                            font=QFont("Ink Free", 20, weight=QFont.Weight.Bold))
        layout.addWidget(self.title)
        
        self.artist = QLabel("None",
                             alignment=Qt.AlignmentFlag.AlignCenter,
                             font=QFont("Ink Free", 10))
        self.artist.setStyleSheet("color: gray;")
        layout.addWidget(self.artist)

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
        track_name, artist_name, album_cover = self.sp.get_current_song()
        if album_cover:
            self.album_cover.setPixmap(album_cover)
        if track_name and artist_name:
            self.artist.setText(artist_name)
            self.title.setText(track_name)