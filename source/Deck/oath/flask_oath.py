import os
import base64
import requests
from flask import Flask, request

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

PORT = 8888

app = Flask(__name__)

# Spotify API URLs
TOKEN_URL = 'https://accounts.spotify.com/api/token'

@app.route('/')
def index():
    """Home page of the Flask server"""
    return 'Flask server is running!'

@app.route('/callback')
def callback():
    """Handle the OAuth callback from Spotify"""
    auth_code = request.args.get('code')  # Get the authorization code from the URL

    if not auth_code:
        return "Error: Authorization code not found in callback", 400

    # Exchange the authorization code for tokens
    access_token, refresh_token = get_tokens(auth_code)

    if access_token:
        # Successfully got tokens, now redirect or show status
        return f"Tokens received! Access Token: {access_token[:10]}..."
    else:
        return "Error retrieving tokens.", 400

def get_tokens(code):
    """Exchange authorization code for access and refresh tokens"""
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
        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']
        # Here you can store the tokens securely or return them
        return access_token, refresh_token
    else:
        print(f"Error fetching tokens: {response.status_code}")
        return None, None

if __name__ == '__main__':    
    app.run(port=PORT)
