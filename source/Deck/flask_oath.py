from flask import Flask, request, jsonify, redirect
from dotenv import load_dotenv, set_key, dotenv_values
import os
import requests

# Load environment variables
load_dotenv()
ENV_FILE = ".env"

app = Flask(__name__)

def store_access_token(token):
    """Save the access token in .env"""
    set_key(ENV_FILE, "ACCESS_TOKEN", token)

@app.route("/login")
def login():
    """Redirects user to Spotify login"""
    CLIENT_ID = os.getenv("CLIENT_ID")
    REDIRECT_URI = os.getenv("REDIRECT_URI")

    AUTH_URL = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=user-read-playback-state%20user-modify-playback-state%20user-read-currently-playing"
    print (AUTH_URL)
    return redirect(AUTH_URL)

@app.route("/callback")
def callback():
    """Handles Spotify login callback and stores token"""
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = os.getenv("REDIRECT_URI")

    auth_code = request.args.get("code")
    if not auth_code:
        return "Error: Authorization code not found", 400

    # Exchange the code for an access token
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    
    response = requests.post(token_url, data=payload)
    token_data = response.json()

    access_token = token_data.get("access_token")
    if access_token:
        store_access_token(access_token)  # Save in .env
        return "Login successful! You can close this window."

    return "Error retrieving access token", 400

@app.route("/token_status")
def token_status():
    """Check if the access token is available"""
    token = os.getenv("ACCESS_TOKEN")
    return jsonify({"logged_in": bool(token)})

if __name__ == "__main__":
    app.run(port=8888, debug=True)
