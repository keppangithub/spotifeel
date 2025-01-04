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
        
        self.base_url = 'https://api.spotify.com/v1'
        self.token_url = 'https://accounts.spotify.com/api/token'
        
            
    def is_user_logged_in(self) -> None:
        '''
        Check if user is logged in by seeing if a code has been generated from the redirectToAuthCodeFlow method.
        
        If the code has not been received, run the redirectToAuthCodeFlow method. Else return.
        '''
        if self.access_token == None:
            return False
        
        else:
            return True
    
    #Authorization Code Flow (https://developer.spotify.com/documentation/web-api/tutorials/code-flow)
    def redirectToAuthCodeFlow(self) -> str:
        '''
        Use spotify's API to create a authorization URL through which a user can login to their Spotify Account (OAuth).
        
        Returns:
        - auth_url
        '''
        scope = 'user-read-private user-read-email'

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
        
        return
    
    def get_auth_header(self):
        '''
        Generates the authorization header for making requests to Spotify API.

        Returns:
        - A dictionary containing the 'Authorization' and 'Content-Type' headers
        '''
        return {'Authorization': 'Bearer ' + self.access_token}
        
    def get_user_information(self):
        '''
        Get information about the logged in user from the SPotify API.
        '''
        url = self.base_url + '/me'
        
        req_header = self.get_auth_header()
        
        response = requests.get(url, headers=req_header)
        user_inf = response.json()
        print(user_inf)
    
        return user_inf
    
    def search_track(self, track, artist):
        '''
        Searcch for a specific track and return its details including
        track ID and URI.

        Parameters:
        - track: str
        - artists: str

        Returns:
        - A dictionary containing the track name, artist, track ID,
            and URI.
        '''
        url = self.base_url + 'search'
        headers = self.get_auth_header()
        query = f'?q=track:"{track}" artist:"{artist}"&type=track&market=US&limit=1'

        query_url = url + query
        result = requests.get(query_url, headers=headers)
        json_result = json.loads(result.content)

        if 'tracks' in json_result and json_result['tracks']['items']:
            track_info = json_result['tracks']['items'][0]
            track_name = track_info['name']
            artist_name = track_info['artists'][0]['name']
            track_id = track_info['id']
            track_uri = track_info['uri']

        if len(json_result) == 0:
            print('No artist with this name exists.')
            return None
        
        return track_name, artist_name, track_id, track_uri
    
    def create_new_playlist(self, user_id: str, new_playlist_name: str):
        '''
        Create a new playlist via Spotify's API.
        
        Parameters:
        - user_id: str 
        - new_playlist_name: str
        
        Returns:
        - 
        '''
        query_url = self.base_url + f'{user_id}/playlists'
        headers = self.get_auth_header()
        
        data = {"name": new_playlist_name}
        
        result = requests.post(query_url, headers=headers, json=data)
        return result
    
    def add_to_playlist(self, playlist_id: str, tracks: list[str]) -> str:
        '''
        Add tracks to a playlist via Spotify's API.
        
        Parameters: 
        - playlist_id: str (ex. 3cEYpjA9oz9GiPac4AsH4n, from spotify)
        - tracks: list of str (ex. spotify:track:1301WleyT98MSxVHPZCA6M, from spotify)
        
        Returns:
        - snapshot_id: str (ex. abc, from spotify)
        
        '''
        query_url = self.base_url + 'playlists/' + f'{playlist_id}/' 
        
        for track_uri in tracks:
            if track_uri != tracks[-1]:
                query_url = query_url + track_uri + ','
                
            else: 
                query_url = query_url + track_uri
        
        headers = self.get_auth_header()
           
        result = requests.post(query_url, headers=headers)
        snapshot_id = json.loads(result.content)
        
        return snapshot_id
    

        
    #Vi struntar i refreshtoken? Överkurs... Mer än 1 h användning typ
    
    
    #Denna behövs ej då den är för serve4r-server, man kan inte få ut user data
    '''
    def get_token(self):
   
        Get access token from spotify for developers which can be used to
        access a given resource or user's data. 

        Returns: 
        token - str

        auth_string = self.client_id + ':' + self.client_secret
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode (auth_bytes), 'utf-8')

        url = 'https://accounts.spotify.com/api/token'
        headers = {
            'Authorization': 'Basic ' + auth_base64,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {'grant_type': 'client_credentials'}
        result = requests.post(url, headers=headers, data=data)
        json_result = json.loads(result.content)

        self.token = json_result['access_token']
        
        return self.token
    '''