from flask import Flask
from spotifyAPI import SpotifyAPI
from clientController import clientController
from emotionController import EmotionController

'''Initialize the Flask application'''
app = Flask(__name__)
app.secret_key = 'enhemlignyckel'

'''Initialize the Controller'''
controller = clientController()

'''Initialize the EmotionController'''
emotionController = EmotionController()

'''Initialize the user object based on the Spotify login'''
user = SpotifyAPI()