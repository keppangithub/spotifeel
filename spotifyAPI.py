from dotenv import load_dotenv
import os
import base64
from requests import post, get
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
        self.token = json_result['access_token']
        return self.token

    def get_auth_header(self):
        return {'Authorization': 'Bearer ' + self.token}
    
    def search_track(self, track, artist):
        url = 'https://api.spotify.com/v1/search'
        headers = self.get_auth_header()
        query = f'?q=remaster%2520{track}%3ADoxy%2520{artist}%3AMiles%2520Davis&type=track%2Cartist&market=US&limit=1&offset=0'

        query_url = url + query
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)

        if 'tracks' in json_result and json_result['tracks']['items']:
            track_info = json_result['tracks']['items'][0]
            track_name = track_info['name']
            artist_name = track_info['artists'][0]['name']

        if len(json_result) == 0:
            print('No artist with this name exists.')
            return None
        return {'track_name': track_name, 'artist_name': artist_name}

spotifyapi = SpotifyAPI()
token = spotifyapi.get_token()
song = spotifyapi.search_track('Baby', 'Justin Bieber')
print(song)