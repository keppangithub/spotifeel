import os

file_name="playlist.txt"
playlists = []
id = 0

if os.path.exists(file_name):
    with open(file_name, 'r') as file:
        playlists = file.readlines()
        last_entry = playlists[-1]
        id = int(last_entry.split(",")[0])


def add_to_playlist(uri):
    global id 
    playlist = {id, uri}
    playlists.append(playlist)
    id+=1
    with open(file_name, 'a') as file:
        file.write(f"{id},{uri}\n")

