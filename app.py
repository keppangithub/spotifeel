from flask import Flask
from API.spotifyAPI import SpotifyAPI

'''Initialize the Flask application'''
app = Flask(__name__)
app.secret_key = 'enhemlignyckel'

'''Initialize the user object based on the Spotify login'''
user = SpotifyAPI()
