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
        
        Attributes:
            client_id (str): The client ID for the Spotify API.
            client_secret (str): The client secret for the Spotify API.
            redirect_uri (str): The redirect URI used for Spotify OAuth authentication.
            auth_endpoint (str): The authorization endpoint URL for the Spotify API.
            access_token (str): The OAuth access token for Spotify API.
            refresh_token (str): The OAuth refresh token for Spotify API.
            base_url (str): The base URL for Spotify's API.
            token_url (str): The token URL for Spotify's OAuth token exchange.
            user_id (str): The user ID for the authenticated Spotify user.
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

    def set_access_token(self, token: str) -> None:
        '''
        Set value of the object property acess_token to the value of the token recived through Spotify's API.
        
        Arg:
            token (str): the users acccess token.
        
        Returns:
            void
        '''
        self.access_token = token


    def get_user_information(self) -> None:
        '''
        Get the user_id for the logged in user from Spotify's API.
        Store the user id in self.user_id

        Returns:
            void
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

        Args:
            user_id (str): user ID.
            new_playlist_name (str): the name of the new playlist.

        Returns:
            str: the ID of the newly created playlist
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
    

    def add_tracks_to_playlist(self, playlist_id: str, tracks_json: dict):
        '''
        Add tracks to a playlist via Spotify's API.
        
        Args:
            playlist_id (str): the playlist ID (ex. 3cEYpjA9oz9GiPac4AsH4n, from spotify).
            tracks_data (dict): JSON-formatted list of tracks, where each track includes 'titel' (song title) and 'artists' (song artist).
        
        Returns:
            list: song info in a dictionary (title, artist, image_url), or False if an error occurs.
        '''
        query_url = f"{self.base_url}/playlists/{playlist_id}/tracks"
        req_header = self.get_auth_header()
        collected_uris = []
        song_info = []
        
        for track in tracks_json:
            title = track.get("titel", "").strip()
            artist = track.get("artists", "").strip()
            
            if not title or not artist:
                print(f"Track Error: Missing title or artist in {track}")
                continue
            
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
        
        req_body = {"uris": collected_uris}
        requests.post(query_url, headers=req_header, json=req_body)
        
        return song_info

    
    def search_track(self, query: str) -> str | None:
        '''
        Search for a track via Spotify's API.

        Args:
            query (str): a query.

        Returns:
            A track_id or None if not found.
        '''
        url = f"{self.base_url}/search"

        req_params = {
            "q": query,
            "type": "track",
            "limit": 1
        }

        req_header = self.get_auth_header()

        try:
            result = requests.get(url, headers=req_header, params=req_params)

            if result.status_code == 200:
                data = result.json()

                if 'tracks' in data and 'items' in data['tracks']:
                    track_uri = data['tracks']['items'][0]['uri']
                    track_image = data['tracks']['items'][0]['album']['images'][0]['url']

                    return track_uri, track_image


                else:
                    print("No tracks found.")
                    return None, None

            else:
                print(f"Error: {result.status_code}")
                return None, None

        except Exception as e:
            print(f'Error: {e}')
            return None, None
        

    def get_auth_header(self) -> dict:
        '''
        Generate the authorization header for making requests to Spotify's API.

        Returns:
            dictionary: containing the 'Authorization' header.
        '''
        return {'Authorization': 'Bearer ' + self.access_token}