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

def load_playlists_txt():
    '''
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

def get_loaded_playlist():
    '''
    '''
    return load_playlists_txt()

def get_playlists():
    '''
    '''
    return playlists


def add_to_playlist(uri):
    '''
    '''
    global id 
    playlist = {'id': id, 'uri': uri}
    playlists.append(playlist)
    
    with open(file_name, 'w') as file:
        json.dump(playlists, file, indent=4)
    id+=1



def get_playlists_by_id(search_id : int):
    '''
    '''
    for playlist in playlists:
        if playlist['id'] == search_id:
            print("playlist found")
            return playlist['uri']
        
    return 'No playlist found'
