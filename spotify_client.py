from dotenv import load_dotenv
import os 
import base64
import requests
import json

load_dotenv()

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

REDIRECT_URI = "http://localhost:5000/callback"
SPOTIFY_AUTH_URL = "https://accoutns.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accoutns.spotify.com/api/token"
SPORIFY_API_BASE_URL = "https://api.spotify.com"

# Get access token
def get_token():
    auth_string = spotify_client_id + ":" + spotify_client_secret 
    # Base64 requires bytes
    auth_bytes = auth_string.encode("utf-8")
    # HTTP headers can only contain text, so we turn back to string
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    # Send request to: 
    # HTTP POST headers: 
    headers = {
        "Authorization": "Basic " + auth_base64, 
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)

    # Parse result to get token
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token 