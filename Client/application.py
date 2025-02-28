from flask import Flask
from Client.spotifyAPI import SpotifyAPI
from API.Client.clientController import clientController
from API.Client.emotionController import EmotionController

'''Initialize the Flask application'''
app = Flask(__name__)
app.secret_key = 'enhemlignyckel'

'''Initialize the Controller'''
controller = clientController()

'''Initialize the EmotionController'''
emotionController = EmotionController()

'''Initialize the user object based on the Spotify login'''
user = SpotifyAPI()