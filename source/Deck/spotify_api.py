import os
import requests
from dotenv import load_dotenv
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QByteArray

# Load environment variables
load_dotenv()

class SpotifyAPI:
    BASE_URL = "https://api.spotify.com/v1/me/player"

    def __init__(self):
        self.access_token = os.getenv("ACCESS_TOKEN")

    def refresh_token(self):
        """Refresh the access token if needed."""
        print("Refreshing access token...")
        requests.get("http://localhost:8888/callback")
        self.access_token = os.getenv("ACCESS_TOKEN")

    def get_current_song(self):
        """Fetch the currently playing song."""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{self.BASE_URL}/currently-playing", headers=headers)

        if response.status_code == 200 and response.json():
            data = response.json()
            track_name = data["item"]["name"]
            artist_name = data["item"]["artists"][0]["name"]
            album_cover = self.get_album_cover(data["item"]["album"]["images"][0]["url"])
            return track_name, artist_name, album_cover
        elif response.status_code == 401 and response.json():
            self.refresh_token()
        else:
            print(response)
            
        return None,None,None
    
    def get_album_cover(self, url:str) -> QPixmap:
        """Fetch the album cover image."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            album_cover = QImage.fromData(QByteArray(response.content)).scaled(320, 320)
            if album_cover.isNull():
                raise ValueError("Failed to load image from URL")
            return QPixmap.fromImage(album_cover)
            
        except Exception as e:
            print(f"Error fetching album cover: {e}")
            return None

    def play(self):
        """Send play request to Spotify."""
        #https://developer.spotify.com/documentation/web-api/reference/start-a-users-playback
        headers = {"Authorization": f"Bearer {self.access_token}"}
        requests.put(f"{self.BASE_URL}/play", headers=headers)

    def pause(self):
        """Send pause request to Spotify."""
        #https://developer.spotify.com/documentation/web-api/reference/pause-a-users-playback
        headers = {"Authorization": f"Bearer {self.access_token}"}
        requests.put(f"{self.BASE_URL}/pause", headers=headers)
        
    def skip(self):
        """Send skip request to Spotify."""
        #https://developer.spotify.com/documentation/web-api/reference/skip-users-playback-to-next-track
        headers = {"Authorization": f"Bearer {self.access_token}"}
        requests.post(f"{self.BASE_URL}/next", headers=headers)
    
    def previous(self):
        """Send previous track request to Spotify."""
        #https://developer.spotify.com/documentation/web-api/reference/skip-users-playback-to-previous-track
        headers = {"Authorization": f"Bearer {self.access_token}"}
        requests.post(f"{self.BASE_URL}/previous", headers=headers)
        
    def get_playback_state(self):
        """Fetch the current playback state."""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{self.BASE_URL}", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return data["is_playing"]
        elif response.status_code == 401:
            self.refresh_token()
        else:
            print(response)
            
        return False
