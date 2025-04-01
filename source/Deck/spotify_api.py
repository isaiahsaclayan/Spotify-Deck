import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SpotifyAPI:
    BASE_URL = "https://api.spotify.com/v1/me/player"

    def __init__(self):
        self.access_token = os.getenv("ACCESS_TOKEN")

    def refresh_token(self):
        """Refresh the access token if needed."""
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
            album_cover = data["item"]["album"]["images"][0]["url"]
            return track_name, artist_name, album_cover
        elif response.status_code == 401 and response.json():
            self.refresh_token()
            print(response)
            return None, None, None
        else:
            print(response)
        return "No song playing"

    def play(self):
        """Send play request to Spotify."""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        requests.put(f"{self.BASE_URL}/play", headers=headers)

    def pause(self):
        """Send pause request to Spotify."""
        headers = {"Authorization": f"Bearer {self.access_token}"}
        requests.put(f"{self.BASE_URL}/pause", headers=headers)
