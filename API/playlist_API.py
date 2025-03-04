from flask import jsonify
from spotify_API import Spotify_API_TMP
from datetime import date
import playlists as playlists

def get_playlist():
    '''
    Check if any playlists have been created and loaded into the system.
    Retrieve the list of loaded playlists.

    Returns:
        Response: A JSON response containing the list of loaded playlists if successful, or an error message with the appropriate HTTP status code.

    Error Handling:
        - 401: If no playlists have been created or loaded into the system.
    '''
    playlist = playlists.get_playlists()
    
    if (1 > len(playlist)):
        return jsonify({"error": "No playlist has been created"}), 401
    
    return jsonify(playlist), 200

def get_playlist_id(id):
    '''
    Retrieve a playlist by its ID.

    Args:
        id (int): a playlist ID.

    Returns:
        Response: A JSON response containing the requested playlist if successful, or an error message with the appropriate HTTP status code.

    Error Handling:
        - 401: If no playlist has been created or the provided ID is invalid.
    '''
    playlist = playlists.get_playlists()
    if (1 > len(playlist)):
        return jsonify({"error": "No playlist has been created"}), 401
    
    if not (0 <= id <= len(playlist)):
        return jsonify({"error": "Invalid playlist ID"}), 401

    playlist = playlists.get_playlists()
    playlist_id = int(id)
    
    return jsonify(playlist[playlist_id]), 200

def post_playlist(access_token, songs_for_playlist):
    '''
    Create a new playlist and add tracks to it based on the provided data.

    Args:
        access_token (str): The access token used for authenticating the user with the Spotify API.
        songs_for_playlist (dict): A dictionary containing the following keys:
            - 'name': The name of the playlist to be created.
            - 'tracks': A list of track IDs to be added to the playlist.

    Returns:
        dict: A dictionary containing the playlist ID of the newly created playlist as well as the list of tracks added.
    '''
    
    user = Spotify_API_TMP()
    user.set_access_token(access_token)
    user.get_user_information()
    
    name = str(songs_for_playlist.get('name'))

    today = date.today()
    new_playlist_id = user.create_new_playlist(user.user_id, f'{name} - {today}')
    uri = str(new_playlist_id)
    tracks = user.add_tracks_to_playlist(new_playlist_id, songs_for_playlist.get('tracks'))
    json_data = {'playlist_id' : new_playlist_id, 'tracks' : tracks}
    playlists.add_to_playlist(uri)
    return json_data

def validate_playlist_json(json_data):
    '''
    Validates the structure and content of the given playlist JSON data.

    Args:
        json_data (dict): A dictionary representing the playlist data, which must include:
            - 'name': The name of the playlist (str).
            - 'tracks': A list of songs to be added to the playlist. Each song must include:
                - 'titel': The title of the song (str).
                - 'artists': The artist(s) of the song (string).

    Returns:
        str or bool: 
            - A string describing the error if the format is invalid.
            - `True` if all checks pass and the format is correct.
    '''
    if not json_data or not isinstance(json_data, dict):
        return 'Json data is not valid'
    
    if not all(key in json_data for key in ['name', 'tracks']):
        return 'Playlist format is not correct'
    
    if not isinstance(json_data['tracks'], list):
        return 'Songs is not a list'
    
    for tracks in json_data['tracks']:
        if not all(key in tracks for key in ['titel', 'artists']):
            return 'Song format is not correct'

    return True 

