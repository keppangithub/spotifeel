from API.spotify_API_TMP import Spotify_API_TMP
from datetime import date



def get_playlist():
        return

def get_playlist_id():
        return

def post_playlist(access_token, songs_for_playlist):
    user = Spotify_API_TMP();
    user.set_access_token(access_token)
    user.get_user_information()

    today = date.today()
    '''LÄGG TILL CORRECT KOPPLING TILL KÄNSLOR FÖR EFTER MERG MED MUNTHER'''
    new_playlist_id = user.create_new_playlist(user.user_id, f'{feeling.capitalize()} - {today}')

    '''SE TILL SÅ FORMATERING ÄR RÄTT MOT JSON OBJEKT'''
    user.add_to_playlist(new_playlist_id, songs_for_playlist)

    return 


def validate_playlist_json(json_data):
    # Kontrollera om json_data är ett objekt och inte None
    if not json_data or not isinstance(json_data, dict):
        return 'Json data is not valid'
    
    # Kontrollera om playlist-objektet finns och har rätt struktur
    if not all(key in json_data for key in ['id', 'uri', 'songs']):
        return 'Playlist format is not correct'
    
    # Kontrollera om songs är en lista
    if not isinstance(json_data['songs'], list):
        return 'Songs is not a list'
    
    # Kontrollera varje låt i listan
    for song in json_data['songs']:
        # Kontrollera om varje låt har alla nödvändiga attribut
        if not all(key in song for key in ['track', 'uri', 'id', 'artists']):
            return 'Song format is not correct'
        
        # Kontrollera om artists är en lista
        if not isinstance(song['artists'], list):
            return 'Artist is not a list'
        
        # Kontrollera varje artist i listan
        for artist in song['artists']:
            # Kontrollera om artist har namn
            if 'name' not in artist:
                return 'Artist is missing name'
    
    # Om alla kontroller passerat, returna True
    return True 

