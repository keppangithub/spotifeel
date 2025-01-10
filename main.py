from flask import Flask, redirect, render_template, request, jsonify, url_for, session
from datetime import date
import promptGPT
import feelings
import spotifeelAPI
from app import app, user
from flask_swagger_ui import get_swaggerui_blueprint

'''Set the path for Swagger documentation'''
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

''' Configure Swagger UI blueprint with application name '''
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Spotifeel API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix='/swagger')

@app.route('/login')
def login_page():
    '''Return template login.html'''
    return render_template('login.html')

@app.route('/oauth_spotify')
def oauth_spotify():
    '''
    Get auth_url via the login() function in the class SpotifyApi

    Redirect user to the login Spotify's login via Spotify API

    '''
    auth_url = user.redirectToAuthCodeFlow()
    return redirect(auth_url)

@app.route('/callback')
def login_callback():
    '''
    The user has been redirected to this endpoint after having logged in to Spotify
    
    Check if the code has been received from the method redirectToAuthCodeFlow() from the class SpotifyApi
    Exchange the received code with an access token via the method login_callback() from the class SpotifyApi

    Redirect user to the index page

    '''
    if 'error' in request.args:
            return jsonify({'error': request.args['error']})

    if 'code' in request.args:
        code = request.args['code']
        user.login_callback(code)
        
        return redirect('/')

@app.route('/', methods=['POST', 'GET'])
def index():
    '''
    Check if user is logged in.
    If the user is not logged in redirect them to the login page.
    
    Else get and store userID in object.
    
    If GET, Get todays date and return chat page. 
    If POST, Get user diary input and run the prompt via OPEN AI API and redirect user to the verify page. 
      
    '''
    if not user.is_user_logged_in():
        print("ERROR: user is not logged in")
        return redirect ('/login')

    else:
        user.get_user_information()
        if request.method == 'POST':
            userPrompt = request.form.get('userPrompt')
            response = promptGPT.run_prompt(userPrompt)
            
            return redirect(url_for('verify', response=response))

        today = date.today()
        return render_template('chat.html', today=today)

@app.route('/playlist', methods=['POST'])
def playlist():
    '''
    Check if user is logged in.
    If the user is not logged in redirect them to the login page.
    
    Check if the user choose to stay in the feeling or wanted the opposite feeling.
    Create a playlist based on the choosen feeling. 
    
    returns:
    - if not logged in: return redirect to login.html
    - if logged in: return redirect to playlist.html
    
    '''
    if not user.is_user_logged_in():
        print("ERROR: user is not logged in")
        return redirect ('/login')
    
    else:
        data = request.get_json()
        action = data.get("message")
        feeling = session.get('feeling')
        
        if action == "false":
            feeling = feelings.negated_feeling(feeling)

        #Create playlist, OPEN & Spotify work together
        today = date.today()
        user.get_user_information()
        songs_for_playlist = promptGPT.create_playlist(feeling)
        
        new_playlist_id = user.create_new_playlist(user.user_id, f'{feeling.capitalize()} - {today}')
        user.add_to_playlist(new_playlist_id, songs_for_playlist)
            
        return render_template('playlist.html')

@app.route("/verify")
def verify():
    '''
    returns:
    - verify.html
    '''
    response = request.args.get('response', None)
    
    if response is None:
        return redirect(url_for('index'))
    
    feeling = feelings.get_feelings(response)
    session['feeling'] = response

    if len(feeling) == 3:
        title, button1, button2 = feeling

    else:
        title, button1, button2 = "Error", "Invalid", "Response"
        
    return render_template('verify.html', title=title, button1=button1, button2=button2)

'''Returns a playlist based on the emotionId provided inside the URL'''
@app.route('/playlists/emotion/<int:emotionId>', methods=['GET'])
def get_playlist_api(emotionId):
    #KODEN HÄR MÅSTE FÄRDIGSTÄLLAS FÖR ATT KUNNA FUNGERA SOM AVSETT
    print(f"{emotionId}")
    return(promptGPT.create_playlist(spotifeelAPI.getEmotionById(f"{emotionId}")))

# Starta servern
if __name__ == '__main__':
    app.run(debug=True, port=8888)
