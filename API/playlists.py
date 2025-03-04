import os
import json

file_name = "playlist.json"
playlists = []
id = 0


if not os.path.exists(file_name) or os.path.getsize(file_name) == 0:
    with open(file_name, 'w') as file:
        json.dump([], file)

try:
    with open(file_name, 'r') as file:
        playlists = json.load(file)
        
        if playlists:
            last_entry = playlists[-1]
            id = last_entry['id'] + 1 
except (json.JSONDecodeError, IndexError):
    playlists = []
    id = 0

def get_playlists() -> list:
    '''
    Retrieves the information found in the global variable "playlists" 
    
    Returns:
        A list of dictionaries, each representing a playlist with a playlist 'id' and 'uri'.
    '''
    return playlists

def add_to_playlist(uri: str) -> None:
    '''
    Add a new playlist to the list of playlists.
    Update the global variable id.
    
    Args:
        uri (str): a uri for a specific playlist.
    
    Returns:
        void.
    '''
    global id 
    playlist = {'id': id, 'uri': uri}
    playlists.append(playlist)
    
    try:
        with open(file_name, 'w') as file:
            json.dump(playlists, file, indent=4)
        
        print(f"Successfully added playlist with URI: {uri}")
        
        id += 1
    except IOError as e:
        print(f"Error writing to file {file_name}: {e}")
