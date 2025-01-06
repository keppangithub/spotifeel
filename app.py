from flask import Flask
from spotifyAPI import SpotifyAPI
app = Flask(__name__)
app.secret_key = 'enhemlignyckel'

user = SpotifyAPI()
