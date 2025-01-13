import os, json

file_name="playlist.json"
playlists = []
id = 0

if os.path.exists(file_name):
    with open(file_name, 'r') as file:
        playlists = json.load(file)
        if playlists:
            last_entry = playlists[-1]
            id = last_entry['id'] + 1 


def add_to_playlist(uri):
    global id 
    playlist = {'id': id, 'uri': uri}
    playlists.append(playlist)
    with open(file_name, 'w') as file:
        json.dump(playlists, file, indent=4)
    id+=1


def get_playlists():
    return playlists

def get_playlists_by_id(search_id : int):
    print(search_id)
    for playlist in playlists:
        if playlist['id'] == search_id:
            print("playlist found")
            return playlist['uri']
