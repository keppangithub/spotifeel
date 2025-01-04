from flask import Flask, redirect, render_template, request, jsonify
from spotifyAPI import SpotifyAPI

app = Flask(__name__)

@app.route('/login')
def login_page():
    '''Return template login.html'''
    return render_template('login.html')

@app.route('/oauth_spotify')
def oauth_spotify():
    '''
    Get auth_url via login() function in class SpotifyApi
    
    Redirect user to the login function via Spotify's API
    
    '''
    auth_url = user.redirectToAuthCodeFlow()
    return redirect(auth_url)

@app.route('/callback')
def login_callback():
    '''
    The user has been redirected to this endpoint after having logged in to Spotify 
    
    Redirect user to the index page
    
    '''   
    if 'error' in request.args:
            return jsonify({'error': request.args['error']})
        
    if 'code' in request.args:
        code = request.args['code']
        user.login_callback(code)
        
        return redirect('/')

@app.route('/')
def index():
    if not user.is_user_logged_in():
        print("ERROR: user is not logged in")
        return redirect ('/login')
    
    else:
        information = user.get_user_information()
        print(information)
        return render_template('index.html')
    
@app.route('/playlist')
def playlist():
    return render_template('playlist.html')

# Starta servern
if __name__ == '__main__':
    user = SpotifyAPI()
    app.run(port=8888)
    
#Behöver vi secret key? (Flask sessions)