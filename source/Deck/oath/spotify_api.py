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
REDIRECT_URI = os.environ.get("REDIRECT_URI")

# Spotify API
AUTH_URL = 'https://accounts.spotify.com/authorize'
API_BASE_URL = 'https://api.spotify.com/v1'

# Variables for storing tokens
ACCESS_TOKEN = None
REFRESH_TOKEN = None

def start_oath_flow():
    """Redirect user to Spotify Login web page"""