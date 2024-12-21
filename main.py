from flask import Flask, redirect, request, render_template
from spotifyAPI import SpotifyAPI

app = Flask(__name__)

@app.route('/')
def index():
    '''Return template index.html'''
    return render_template('index.html')

@app.route('/login')
def login():
    auth_url = SpotifyAPI.login()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    SpotifyAPI.login_Callback()