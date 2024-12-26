from dotenv import load_dotenv
import os
import urllib.parse
import base64
from requests import post, get, request
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
        
        self.token = None
        
        self.base_url = 'https://api.spotify.com/v1/'
        self.token_url = 'https://accounts.spotify.com/api/token'
        self.redirect_uri = 'http://localhost:8888/callback'
        self.auth_url = 'https://accounts.spotify.com/authorize'

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
        '''
        Generates the authorization header for making requests to
        Spotify API.

        Returns:
        - A dictionary containing the 'Authorization' and
            'Content-Type' headers
        '''
        return {'Authorization': 'Bearer ' + self.token, 
                'Content-Type' : 'application/json'}
        
    def login(self):
        '''
        Use spotify's API to create a authorization URL through which a user can login to their Spotify Account (OAuth).
        
        Returns:
        - auth_url
        '''
        scope = 'user-read-private user-read-email'

        query_params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'scope': scope, 
            'redirect_uri': self.redirect_uri,
        }
        
        auth_url = self.auth_url + '?' + urllib.parse.urlencode(query_params)
        return auth_url
    
    def login_callback(self, request): 
        '''
        Get acess token, refresh token and information about when the token expires from SpotifyAPI.
        Redirect the user to the defined redirect_uri. 
        
        Returns:
        - String with:
           - acess_token
           - refresh_token
           - expires_in
        '''     
        
        code = request.args.get('code')
        
        if not code:
            return "Authorization code missing from the request"
    
        response = post(self.token_url, data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        })
        
        if response.status_code != 200:
            return f"Error exchanging code for token: {response.status_code}"
        
        token_info = response.json()
        
        access_token = token_info.get('access_token')
        refresh_token = token_info.get('refresh_token')
        expires_in = token_info.get('expired_in')
        

        return f'Access Token: {access_token}, Refresh Token: {refresh_token}, Token info: {expires_in}'
        
    
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
        result = get(query_url, headers=headers)
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
        
        result = post(query_url, headers=headers, json=data)
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
           
        result = post(query_url, headers=headers)
        snapshot_id = json.loads(result.content)
        
        return snapshot_id
                       
spotifyapi = SpotifyAPI() 
token = spotifyapi.get_token()
song = spotifyapi.search_track('Baby', 'Justin Bieber')
print(song)
#print(spotifyapi.create_new_playlist('i1217ccdaax1rwrq588j1ymax', 'Ellen test'))