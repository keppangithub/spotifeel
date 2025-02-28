from app import app
from spotifyAPI import SpotifyAPI
from emotionController import EmotionController

'''Initialize the EmotionController'''
emotionController = EmotionController()

'''Initialize the user object based on the Spotify login'''
user = SpotifyAPI()