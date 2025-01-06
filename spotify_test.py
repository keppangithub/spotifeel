import os
from flask import Flask, redirect, request, session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotifeel

# Your Spotify application credentials
CLIENT_ID = '752df86356504cff94ef280e40b0a2c4'
CLIENT_SECRET = '3aca6de943994c13be870ab0092e2b15'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
SCOPE = 'user-library-read user-read-private playlist-modify-private playlist-modify-public'  # Adjust the scope depending on the permissions you need

app = Flask(__name__)

# Set a secret key to enable session functionality
app.secret_key = 'your_secret_key'

# Initialize the SpotifyOAuth object
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         redirect_uri=REDIRECT_URI,
                         scope=SCOPE)

@app.route('/')
def home():
    return redirect(sp_oauth.get_authorize_url())  # Redirect the user to Spotify's login page

@app.route('/callback')
def callback():
    # Spotify redirects to this route with an authorization code
    token_info = sp_oauth.get_access_token(request.args['code'])
    session['token_info'] = token_info  # Store the token information in the session
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    # Get the access token from the session
    token_info = session.get('token_info', None)

    if not token_info:
        return redirect('/')

    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    # Fetch the user's profile
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

# Step 3: Add tracks to the playlist
    song_strings = ["Lean On Me by Bill Withers", "Three Little Birds by Bob Marley"]

# Step 1: Convert song names to track URIs
    track_uris = []
    for song in song_strings:
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
    
    return f"Hello {user_profile['display_name']}!<br>Your Spotify username: {user_profile['id']}"

if __name__ == '__main__':
    app.run(debug=True)