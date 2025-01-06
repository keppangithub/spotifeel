from dotenv import load_dotenv
from openai import OpenAI
import os
from spotipy.oauth2 import SpotifyOAuth
from datetime import date
import spotipy
load_dotenv()
key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=key)
      

def run_prompt(text):
    completion = client.chat.completions.create(
     model="gpt-3.5-turbo",
         messages=[
        {"role": "system", "content": "Your task is to determine which of the following feelings, and only one of the following feeling suits the text the most: furious, frustrated, horrified, disappointed, euphoric, loving, happy, useless, regretful, dejected, unhappy, scared, and anxious. Respond with only one of these words in english and without capital letters."},
        {
            "role": "user",
            "content":'"'+text+'"'
        }
] 
)
    response_content = completion.choices[0].message
    emotion = str(response_content).split("content='")[1].split("'")[0]
    print(emotion)
    return emotion


def create_playlist(emotion, token_info):
    completion = client.chat.completions.create(
     model="gpt-3.5-turbo",
         messages=[
        {"role": "system", "content": "Your task is to give 6 recomendations for songs that can be found on spotify based on the emotion you recieve. The recommendations shall follow this structure: song title, artist and ONLY contain this."},
           {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": '"'+emotion+'"'
        }
      ]
    }
] 
)
    
    songs = completion.choices[0].message.content
    songs = [line.split(". ", 1)[1] for line in songs.split("\n")]
    formatted_songs = [
    song.replace('"', '')  # Remove all quotes from the song titles
    for song in songs
   ]

# Optionally, add double quotes around each song name if needed
    formatted_songs = [f'"{song}"' for song in formatted_songs]

    print(formatted_songs)
    sp = spotipy.Spotify(auth=token_info['access_token'])

    user_profile = sp.current_user()
    user = sp.current_user()
    user_id = user['id']  # User's Spotify ID

# Step 2: Create a new playlist
    playlist_name = "My Awesome Playlist 2"
    playlist_description = "This playlist was created using Spotify's API!"
    new_playlist = sp.user_playlist_create(user=user_id, 
                                       name=playlist_name, 
                                       public=False, 
                                       description=playlist_description)

    playlist_id = new_playlist['id']
    print(f"Created playlist '{playlist_name}' with ID: {playlist_id}")


# Step 1: Convert song names to track URIs
    track_uris = []
    for song in formatted_songs:
        results = sp.search(q=song, type='track', limit=1)
    if results['tracks']['items']:
        track_uris.append(results['tracks']['items'][0]['uri'])  # Get the URI of the first result
    else:
        print(f"Track not found: {song}")

# Step 2: Add tracks to the playlist
    if track_uris:
        sp.playlist_add_items(playlist_id, track_uris)
        print(f"Added {len(track_uris)} tracks to the playlist!")
    else:
        print("No valid tracks found to add.")
        
        
    return songs
