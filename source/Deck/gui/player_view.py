from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QTransform
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
        
        control_layout = QHBoxLayout()
        control_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        control_layout.setSpacing(40)
        
        # Album Cover
        self.album_cover = QLabel()
        layout.addWidget(self.album_cover,
                         alignment=Qt.AlignmentFlag.AlignCenter)

        # Title
        self.title = QLabel("No song playing",
                            alignment=Qt.AlignmentFlag.AlignCenter,
                            font=QFont("Segoe UI Variable", 20, weight=QFont.Weight.Bold))
        self.title.setStyleSheet("color: black;")
        self.title.setWordWrap(True)
        layout.addWidget(self.title)
        
        # Artist
        self.artist = QLabel("None",
                             alignment=Qt.AlignmentFlag.AlignCenter,
                             font=QFont("Segoe UI Variable", 15))
        self.artist.setStyleSheet("color: gray;")
        layout.addWidget(self.artist)
        
        # Backwards Button
        transform = QTransform().rotate(180)
        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon("assets/back-track.png"))
        self.back_button.setIconSize(QSize(40,40))
        self.back_button.setStyleSheet("border: none;")
        self.back_button.clicked.connect(self.sp.previous)
        control_layout.addWidget(self.back_button)

        # Pause/Play Button
        self.play_pause_button = QPushButton()
        self.play_pause_button.setIcon(QIcon("assets/pause-button.png"))
        self.play_pause_button.setIconSize(QSize(50,50))
        self.play_pause_button.setStyleSheet("border: none;")
        self.play_pause_button.clicked.connect(self.toggle_playback)  
        control_layout.addWidget(self.play_pause_button)
        
        # Skip Button
        self.skip_button = QPushButton()
        self.skip_button.setIcon(QIcon("assets/skip-track.png"))
        self.skip_button.setIconSize(QSize(40,40))
        self.skip_button.setStyleSheet("border: none;")
        self.skip_button.clicked.connect(self.sp.skip)
        control_layout.addWidget(self.skip_button)
        
        layout.addLayout(control_layout)
        self.setLayout(layout)

        # Configure Timer and Start
        self.song_timer = QTimer(self)
        self.song_timer.timeout.connect(self.update_player)
        self.song_timer.start(1000)
        
        # Configure Refresh Token Timer
        self.token_timer = QTimer(self)
        self.token_timer.timeout.connect(self.sp.refresh_token)
        self.token_timer.start(300000)  # 5 minutes

    def update_player(self):
        track_name, artist_name, album_cover = self.sp.get_current_song()

        if track_name and artist_name:
            self.artist.setText(artist_name)
            self.title.setText(track_name)
            if album_cover:
                self.album_cover.setPixmap(album_cover)
                                
        if self.sp.get_playback_state():
            self.play_pause_button.setIcon(QIcon("assets/pause-button.png"))
        else:
            self.play_pause_button.setIcon(QIcon("assets/play-button.png"))
    
    def toggle_playback(self):
        if self.sp.get_playback_state():
            self.play_pause_button.setIcon(QIcon("assets/pause-button.png"))
            self.sp.pause()
        else:
            self.play_pause_button.setIcon(QIcon("assets/pause-button.png"))
            self.sp.play()
            