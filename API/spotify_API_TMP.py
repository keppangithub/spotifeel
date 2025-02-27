from dotenv import load_dotenv
import os

import urllib.parse
import base64

import requests
import json
class Spotify_API_TMP:
    def __init__(self) -> None:
        '''
        Intialises the SpotifyAPI object by loading environement
        variables and setting up the requored credentials and API URI.
        '''
        load_dotenv()

        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')

        self.redirect_uri = 'http://localhost:8888/callback'
        self.auth_endpoint = 'https://accounts.spotify.com/authorize'

        self.access_token = None
        self.refresh_token = None

        self.base_url = 'https://api.spotify.com/v1'
        self.token_url = 'https://accounts.spotify.com/api/token'

        self.user_id = None

    def set_access_token(self, token):
        self.access_token = token


    def get_user_information(self) -> None:
        '''
        Get the user_id for the logged in user from the SPotify API.
        Store the user id in self.user_id

        Returns:
        - void
        '''
        url = self.base_url + '/me'

        req_header = self.get_auth_header()

        response = requests.get(url, headers=req_header)
        response = response.json()

        self.user_id = response['id']

        return
    

    def create_new_playlist(self, user_id: str, new_playlist_name: str) -> str:
        '''
        Create a new playlist via Spotify's API.

        Parameters:
        - user_id: str
        - new_playlist_name: str

        Returns:
        - playlist_id (str)
        '''

        query_url = self.base_url + f'/users/{user_id}/playlists'
        req_headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/json'
            }

        req_data = {
            'name': new_playlist_name
            }
        
        result = requests.post(query_url, headers=req_headers, json=req_data)
        result_json = result.json()
        playlist_id = result_json['id']

        return playlist_id
    
    def add_to_playlist(self, playlist_id: str, tracks: list[str]) -> str:
        '''
        Add tracks to a playlist via Spotify's API.

        Parameters:
        - playlist_id: str (ex. 3cEYpjA9oz9GiPac4AsH4n, from spotify)
        - tracks: list of str (ex. spotify:track:1301WleyT98MSxVHPZCA6M, from spotify)

        Returns:
        - void
        '''
        query_url = f"{self.base_url}/playlists/{playlist_id}/tracks"
        req_header = self.get_auth_header()

        collected_uris = []
        song_info = []

        for track in tracks:
            for i in track:
                if ',' in i:
                    title, artist = i.split(',', 1)

                elif '-' in i:
                    title, artist = i.split('-', 1)

                else:
                    print(f"Track Error: Invalid format from OPEN AI")
                    return False

                title = title.strip()
                artist = artist.strip()

                query = f"track:{title} artist:{artist}"

                uri, image_url = self.search_track(query)

                if uri:
                    collected_uris.append(uri)
                    song_info.append({
                        'title': title,
                        'artist': artist,
                        'image_url': image_url
                    })


            if not collected_uris:
                print("No valid tracks found to add to playlist")
                return

        req_body = {
            "uris": collected_uris
        }

        requests.post(query_url, headers=req_header, json=req_body)

        return song_info