#pip install spotify-api.py

import os
import base64
from requests import post, get
import json
from dotenv import load_dotenv

class SpotifyAPI:
    def __init__(self) -> None:
        load_dotenv()
        self.__client_id = str(os.getenv("CLIENT_ID"))
        self.__client_secret = str(os.getenv("CLIENT_SECRET"))

    def get_token(self):
        '''Function to get Spotify API token'''
        auth_string = self.__client_id + ":" + self.__client_secret
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {"grant_type": "client_credentials"}
        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        json_result = result.json()
        return json_result["access_token"]
