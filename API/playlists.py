import os, json

file_name="API/playlist.json"
txt_file="API/playlist.txt"
playlists = []
id = 0

if os.path.exists(file_name):
    with open(file_name, 'r') as file:
        playlists = json.load(file)
        
        if playlists:
            last_entry = playlists[-1]
            id = last_entry['id'] + 1 

def load_playlists_txt() -> list:
    '''
    Load playlists from the textfile playlists.txt and parse them into a list of dictionaries.
    Update global variables. 
    
    Global variables:
        - playlists: A list of dictionaries, each containing 'id' and 'uri' for a playlist.
        - id: The next available playlist ID, which is one greater than the maximum existing ID in the file.

    Returns:
        list: A list of dictionaries, each representing a playlist with a playlist 'id' and 'uri'.
        If an error occurs an empty list is returned.
    '''
    global playlists, id
    
    if os.path.exists(txt_file):
        try:
            with open(txt_file, 'r', encoding='utf-8') as file:
                playlists = []
                for line in file:
                    if line.strip():  # Skip empty lines
                        playlist_id, uri = line.strip().split(',')

                        playlists.append({
                            'id': int(playlist_id),
                            'uri': uri
                        })
                        
                if playlists:
                    id = max(p['id'] for p in playlists) + 1
                    
                return playlists
            
        except Exception as e:
            print(f"Error loading playlists: {e}")
            return []
        
    return []

def get_loaded_playlist() -> list:
    '''
    Retrieves the loaded playlists by calling the load_playlists_txt function.

    Returns:
        list: A list of dictionaries, each representing a playlist with a playlist 'id' and 'uri'.
        If an error occurs an empty list is returned.
    '''
    return load_playlists_txt()

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
    
    with open(file_name, 'w') as file:
        json.dump(playlists, file, indent=4)
    with open(txt_file, 'w', encoding='utf-8') as file:
        for playlist in playlists:
            file.write(f"{playlist['id']},{playlist['uri']}\n")
        
    id+=1

def get_playlists_by_id(search_id : int) -> str:
    '''
    Search for a playlist with a specific ID.

    Args:
        search_id (int): playlist ID.

    Returns:
        str: The URI of the playlist, or a message saying 'No playlist found' if not found.
    '''
    for playlist in playlists:
        if playlist['id'] == search_id:
            return playlist['uri']
        
    return 'No playlist found'
