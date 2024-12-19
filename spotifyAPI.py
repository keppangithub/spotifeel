from dotenv import load_dotenv
import os
import base64
from requests import post
import json

class SpotifyAPI:
    def __init__(self) -> None:
        load_dotenv()
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.token = None

    def get_token(self):
        '''
        Get access token from spotify for developers which can be used to
        access a given resource or user's data. 

        Returns: 
        token - str
        '''
        auth_string = self.client_id + ':' + self.client_secret
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode (auth_bytes), 'utf-8')

        url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Authorization': 'Basic ' + auth_base64,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {'grant_type': 'client_credentials'}
        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result['access_token']
        return token

    def get_auth_header(token):
        return {'Authorization': 'Beare ' + token}

spotifyapi = SpotifyAPI()
token = spotifyapi.get_token()