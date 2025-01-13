import os

file_name="playlist.txt"
playlists = []
id = 0

if os.path.exists(file_name):
    with open(file_name, 'r') as file:
        playlists = file.readlines()
        if playlists:
            last_entry = playlists[-1]
            id = int(last_entry.split(",")[0])


def add_to_playlist(uri):
    global id 
    playlist = [id, uri]
    playlists.append(playlist)
    with open(file_name, 'a') as file:
        file.write(f"{id},{uri}\n")
    id+=1


def get_playlists():
    return playlists

def get_platlists_by_id(search_id):
    return playlists(search_id)

