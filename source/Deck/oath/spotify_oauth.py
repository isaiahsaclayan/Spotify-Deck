import webbrowser
import requests
import base64
import urllib
import os
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtGui import QDesktopServices

# Spotify credentials
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

# Spotify API
REDIRECT_URI = 'http://127.0.0.1:8000/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
SCOPE = 'user-library-read user-read-playback-state user-modify-playback-state'

# Variables for storing tokens
ACCESS_TOKEN = None
REFRESH_TOKEN = None

def start_oath_flow():
    pass