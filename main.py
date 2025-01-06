from flask import Flask, redirect, render_template, request, jsonify, url_for, session
from spotipy.oauth2 import SpotifyOAuth
from datetime import date
import promptGPT, spotipy
import feelings

app = Flask(__name__)
app.secret_key = 'enhemlignyckel'

CLIENT_ID = '752df86356504cff94ef280e40b0a2c4'
CLIENT_SECRET = '3aca6de943994c13be870ab0092e2b15'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
SCOPE = 'user-library-read user-read-private playlist-modify-private playlist-modify-public'

sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         redirect_uri=REDIRECT_URI,
                         scope=SCOPE)



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
    return redirect(sp_oauth.get_authorize_url()) 

@app.route('/callback')
def login_callback():
    token_info = sp_oauth.get_access_token(request.args['code'])
    session['token_info'] = token_info 
    return redirect('/')

@app.route('/', methods=['POST', 'GET'])
def index():
            # Get the access token from the session
        token_info = session.get('token_info', None)

        if not token_info:
            return redirect('/login')

        sp = spotipy.Spotify(auth=token_info['access_token'])
        if request.method == 'POST':
            userPrompt = request.form.get('userPrompt')
            response = promptGPT.run_prompt(userPrompt)
            return redirect(url_for('verify', response=response))
        
        today = date.today()
        return render_template('chat.html', today=today)
    
@app.route('/playlist', methods=['POST'])
def playlist():
    data = request.get_json()
    action = data.get("message")
    feeling = session.get('feeling')    
    print("This should be either true or false: "+ action)
    print("This is the feeling in /playlist:"+feeling)
    if action == "false":
        feeling = feelings.negated_feeling(feeling)
        print("This is the negated feeling:" + feeling)

    token_info = session.get('token_info', None)
    promptGPT.create_playlist(feeling, token_info)

    return render_template('playlist.html')



@app.route("/verify")
def verify():
    response = request.args.get('response', None)
    if response is None:
        return redirect(url_for('index'))
    print("This is the response:" + response)
    feeling = feelings.get_feelings(response)
    session['feeling'] = response
    print(feeling)
    if len(feeling) == 3:
        title, button1, button2 = feeling
        print(title)
    else:
        title, button1, button2 = "Error", "Invalid", "Response"
    return render_template('verify.html', title=title, button1=button1, button2=button2)

# Starta servern
if __name__ == '__main__':
    app.run(debug=True)
    