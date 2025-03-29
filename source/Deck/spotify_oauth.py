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

def get_authorization_url():
    """
    Returns the URL for user to authorize the app
    """
    auth_params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope' : SCOPE,
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(auth_params)}"

    return auth_url

def get_tokens(code):
    """
    Exchange authorization code for access and refresh tokens
    """
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code == 200:
        tokens = response.json()
        global ACCESS_TOKEN, REFRESH_TOKEN
        ACCESS_TOKEN = tokens['access_token']
        REFRESH_TOKEN = tokens['refresh_token']
        print("Tokens received!")
        return ACCESS_TOKEN, REFRESH_TOKEN
    else:
        print(f"Error retrieving tokens: {response.status_code}")
        return None, None
    
def refresh_access_token():
    """
    Use the refresh token to get a new access token
    """
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code == 200:
        tokens = response.json()
        global ACCESS_TOKEN
        ACCESS_TOKEN = tokens['access_token']
        print("Access token refreshed!")
        return ACCESS_TOKEN
    else:
        print(f"Error refreshing token: {response.status_code}")
        return None