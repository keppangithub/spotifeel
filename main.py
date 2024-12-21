from flask import Flask, redirect, render_template, request
from spotifyAPI import SpotifyAPI

app = Flask(__name__)

@app.route('/')
def index():
    '''Return template index.html'''
    return render_template('login.html')

@app.route('/login')
def login():
    '''
    Get auth_url via login() function in class SpotifyApi
    
    Redirect user to the login function via Spotify's API
    
    '''
    auth_url = user.login()
    print(f'Redirecting to: {auth_url}')
    return redirect(auth_url)

@app.route('/callback')
def login_callback():
    '''
    The user has been redirected to this endpoint after having logged in to Spotify 
    
    Redirect user to the home page
    
    '''   
    return redirect('/home')

@app.route('/home')
def home_page():
    render_template('index.html')


# Starta servern
if __name__ == '__main__':
    user = SpotifyAPI()
    app.run(port=8888)