from flask import Flask, redirect, request, render_template
from dotenv import load_dotenv
import os
import urllib.parse
from requests import post

load_dotenv()

app = Flask(__name__) # egentligen ska man använda mains app eller?

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET') # egentligen ska ju detta hämtas från main
REDIRECT_URI = 'http://localhost:8888/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

@app.route('/')
def index():
    return render_template('index.html')

# När användaren trycker på log-in knappen så skickas användaren till denna route
@app.route('/login')
def login():
    scope = 'user-read-private user-read-email'
    query_params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'scope': scope, 
        'redirect_uri': REDIRECT_URI,
    }
    auth_url = AUTH_URL + '?' + urllib.parse.urlencode(query_params)
    return redirect(auth_url)

# Användaren skickas till denna route efter att ha loggat in på Spotify
@app.route('/callback')
def callback():
    code = request.args.get('code')
    
    response = post(TOKEN_URL, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    response_data = response.json()
    access_token = response_data.get('access_token')

    return f'Access Token: {access_token}'


# Starta servern
if __name__ == '__main__':
    app.run(port=8888)
