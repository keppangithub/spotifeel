from flask import jsonify
from spotify_API import Spotify_API_TMP
from datetime import date
import spotifeelAPI as spotifeel



def get_playlist():
        playlist = spotifeel.get_loaded_playlist()
        if (1 > len(playlist)):
            return jsonify({"error": "No playlist has been created"}), 401
        return jsonify(playlist), 200

def get_playlist_id(id):
    playlist = spotifeel.get_loaded_playlist()
    if (1 > len(playlist)):
        return jsonify({"error": "No playlist has been created"}), 401
    
    if not (1 <= id <= len(playlist)):
        return jsonify({"error": "Invalid playlist ID"}), 401

    playlist = spotifeel.get_loaded_playlist()
    playlist_id = int(id)
    return jsonify(playlist[playlist_id]), 200

def post_playlist(access_token, songs_for_playlist):
    user = Spotify_API_TMP()
    user.set_access_token(access_token)
    user.get_user_information()
    name = str(songs_for_playlist.get('name'))

    today = date.today()
    new_playlist_id = user.create_new_playlist(user.user_id, f'{name} - {today}')

    tracks = user.add_tracks_to_playlist(new_playlist_id, songs_for_playlist.get('tracks'))

    json_data = {'playlist_id' : new_playlist_id, 'tracks' : tracks}
    return json_data


def validate_playlist_json(json_data):
    # Kontrollera om json_data är ett objekt och inte None
    if not json_data or not isinstance(json_data, dict):
        return 'Json data is not valid'
    
    # Kontrollera om playlist-objektet finns och har rätt struktur
    if not all(key in json_data for key in ['name', 'tracks']):
        return 'Playlist format is not correct'
    
    # Kontrollera om songs är en lista
    if not isinstance(json_data['tracks'], list):
        return 'Songs is not a list'
    
    # Kontrollera varje låt i listan
    for tracks in json_data['tracks']:
        # Kontrollera om varje låt har alla nödvändiga attribut
        if not all(key in tracks for key in ['titel', 'artists']):
            return 'Song format is not correct'
    
    # Om alla kontroller passerat, returna True
    return True 

