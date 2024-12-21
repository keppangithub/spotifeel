from flask import Flask, redirect, request, render_template
from spotifyAPI import SpotifyAPI

app = Flask(__name__)

@app.route('/')
def index():
    '''Return template index.html'''
    return render_template('index.html')

@app.route('/login')
def login():
    auth_url = user.login()
    return redirect(auth_url) 

@app.route('/login callback')
def login_callback():
    pass

# Starta servern
if __name__ == '__main__':
    user = SpotifyAPI()
    app.run(port=8888)