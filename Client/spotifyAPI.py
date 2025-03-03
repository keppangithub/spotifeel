from dotenv import load_dotenv
import os

import urllib.parse
import base64

import requests
import json

class SpotifyAPI:
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

    def is_user_logged_in(self) -> bool:
        '''
        Check if user is logged in by seeing if a code has been generated from the redirectToAuthCodeFlow method.

        Returns:
        - Boolean depending on if the token has been generated or not.
        '''
        if self.access_token == None:
            return False

        else:
            return True

    #Authorization Code Flow (https://developer.spotify.com/documentation/web-api/tutorials/code-flow)
    def redirect_to_auth_code_flow(self) -> str:
        '''
        Use spotify's API to create a authorization URL through which a user can login to their Spotify Account (OAuth).

        Returns:
        - auth_url (str)
        '''
        scope = 'user-read-private user-read-email playlist-modify-public playlist-modify-private'

        query_params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'scope': scope,
            'redirect_uri': self.redirect_uri,
        }

        auth_url = self.auth_endpoint + '?' + urllib.parse.urlencode(query_params)
        return auth_url

    def login_callback(self, code):
        '''
        Get acess token by handing in the code gotten from the user authorization from SpotifyAPI.
        Redirect the user to the defined redirect_uri.

        Returns:
        - String with:
           - acess_token
           - refresh_token
           - expires_in
        '''
        auth_string = self.client_id + ':' + self.client_secret
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode (auth_bytes), 'utf-8')

        req_headers = {
            'Authorization': 'Basic ' + auth_base64,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        req_body = {
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }

        response = requests.post(self.token_url, headers=req_headers, data=req_body)
        token_info = response.json()

        self.access_token = token_info.get('access_token')
        self.refresh_token = token_info.get('refresh_token')

        return

    def get_auth_header(self) -> dict:
        '''
        Generates the authorization header for making requests to Spotify API.

        Returns:
        - A dictionary containing the 'Authorization' header (dict)
        '''
        return {'Authorization': 'Bearer ' + self.access_token}

    def get_user_information(self) -> None:
        '''
        Get the user_id for the logged in user from the SPotify API.
        Store the user id in self.user_id

        Returns:
        - void
        '''
        url = self.base_url + '/me'

        req_header = self.get_auth_header()
        
        print(req_header)

        try:
            response = requests.get(url, headers=req_header)
            if response.status_code == 200:

                response = response.json()

                self.user_id = response['id']
                return response.status_code
                
            else:
                print(f"An Error ocurred, Status code: {response.status_code}")
                return response.status_code
            
        except Exception as e:
            print(f"Exception occured: {e}")
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

    def search_track(self, query: str) -> str | None:
        '''
        Search for a track through the Spotify API.

        parameter:
        - query (str)

        returns:
        - None or track_id
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

    def get_user_playlist(self, playlistID):
        query_url = f"{self.base_url}/playlists/{playlistID}"
        req_header = self.get_auth_header()

        response = requests.get(query_url, headers=req_header)
        return response.json()
