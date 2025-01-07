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
        scope = 'user-read-private user-read-email playlist-modify-public'

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
        - playlist id (str)
        '''
        query_url = self.base_url + f'/users/{user_id}/playlists'
        print(query_url)
    
        req_headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'name' : new_playlist_name
            }
        print(new_playlist_name)
        
        req_data = {
            'name': new_playlist_name
            }
        
        result = requests.post(query_url, headers=req_headers, json=req_data)
        print(result)
        
        result = result.json()
        playlist_id = result['id']
        
        return playlist_id
    
    def add_to_playlist(self, playlist_id: str, tracks: list[str]) -> str:
        '''
        Add tracks to a playlist via Spotify's API.
        
        Parameters: 
        - playlist_id: str (ex. 3cEYpjA9oz9GiPac4AsH4n, from spotify)
        - tracks: list of str (ex. spotify:track:1301WleyT98MSxVHPZCA6M, from spotify)
        
        Returns:
        - snapshot_id: str (ex. abc, from spotify)
        
        '''       
        query_url = f"{self.base_url}/playlists/{playlist_id}/tracks"  
        req_header = self.get_auth_header()
        
        collected_uris = []
        
        print(tracks)
        
        for track in tracks:
            print(track)
            for i in track:
                print(i)
                if ',' in i:
                    title, artist = i.split(',', 1)
                    
                elif '-' in i:  
                    title, artist = i.split('-', 1)
                    
                else:
                    print(f"Track Error: Invalid format from OPEN AI")
                
                title = title.strip()
                artist = artist.strip()   
                
                print(title)
                print(artist)
                
                query = f"track:{title} artist:{artist}"
                                
                uri = self.search_track(query)
                if uri:
                    print(f"Found URI: {uri}")
                    collected_uris.append(uri)
                    
            if not collected_uris:
                print("No valid tracks found to add to playlist")
                return
            
        print(collected_uris)
             
        req_body = {
            "uris": collected_uris
        }
            
        requests.post(query_url, headers=req_header, json=req_body)
        
        return collected_uris
    
    def search_track(self, query: str) -> str | None:
        url = f"{self.base_url}/search"
        
        req_params = {
            "q": query,
            "type": "track",
            "limit": 1
        }
        
        print(req_params)
        
        req_header = self.get_auth_header()

        try:
            result = requests.get(url, headers=req_header, params=req_params)
            
            if result.status_code == 200:
                data = result.json()
                
                if 'tracks' in data and 'items' in data['tracks']:
                    track_uri = data['tracks']['items'][0]['uri']
                    return track_uri
                
                else:
                    print("No tracks found.")
                    return None
                
            else:
                print(f"Error: {result.status_code}")
                return None
            
        except Exception as e:
            print(f'Error: {e}')
            return None