from flask import Flask, redirect, render_template, request, jsonify, url_for, session
from datetime import date
import API.promptGPT as promptGPT, feelings, API.spotifeelAPI as spotifeelAPI, API.playlists as playlists
from app import app, user
from flask_swagger_ui import get_swaggerui_blueprint
import os
import requests
import API.playlist_API_TMP as spotifeelAPI_playlist
'''Set the path for Swagger documentation'''
SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'

''' Configure Swagger UI blueprint with application name '''
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Spotifeel API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix='/docs')

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
    Method used to create a playlist using GPT and post to Spotify.
    Check if user is logged in.
    If the user is not logged in redirect them to the login page.

    Check if the user choose to stay in the feeling or wanted the opposite feeling.
    Create a playlist based on the choosen feeling.

    Returns:
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
        song_info = user.add_to_playlist(new_playlist_id, songs_for_playlist)
        display_feeling = feeling.capitalize()


        playlists.add_to_playlist(new_playlist_id)


        return render_template('playlist.html', new_playlist_id=new_playlist_id, song_info=song_info, display_feeling=display_feeling, today=today)

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

@app.route('/emotions', methods=['GET'])
def get_emotions():
    emotion_id = 0;
    data = None;
    prompt = None;
    try:
        data = request.get_json()
        try:
            emotion_id = int(data['emotion_id'])
        except Exception as e:
            print(f"Error: {e}")
        try:
            prompt = str(data['prompt'])
        except Exception as e:
            print(f"Error: {e}")

    except Exception as e:
        print(f"Error: {e}")


    if data is None:
        return jsonify(spotifeelAPI.get_emotions())

    if emotion_id != 0:
        if not (1 <= emotion_id <= 13):
            return jsonify({"error": "Invalid emotion ID"}), 400

        return jsonify(spotifeelAPI.get_emotion_by_id(emotion_id))

    if prompt is not None:
        return jsonify(promptGPT.run_prompt(prompt))


@app.route('/playlist<int:id>', methods=['GET'])
def get_playlists_id(id):
    emotion_id = id;

    


@app.route('/playlists', methods=['GET'])
def get_playlists():
    json_data = None;
    try:
        json_data = request.get_json()
        playlist_id = int(json_data['playlist_id'])
    except Exception as e:
        print(f"Error: {e}")

    if json_data is None:
        return jsonify(spotifeelAPI.get_loaded_playlist()), 201
    else:
        playlist = spotifeelAPI.get_loaded_playlist()
        try:
            return jsonify(playlist[playlist_id])
        except Exception as e:
            return jsonify({"error" : "Invalid id"})


@app.route('/playlists', methods=['POST'])
def post_playlists():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid authorization token"}), 401
    
    access_token = auth_header.split(' ')[1]
    try:
        json_data = request.get_json(force=True)
        if not json_data:
            return jsonify({"error": "Request must be Json"}), 400
        
        validate_data = spotifeelAPI_playlist.validate_playlist_json(json_data)
        if validate_data is True:
            return jsonify({spotifeelAPI_playlist.post_playlist(access_token, json_data)}), 201
        else:
            return jsonify({"error": validate_data}), 400
        
    except Exception as e:
        return jsonify({"error": "Unexpected error"}), 500




'''
Starting server with port - 8888
'''
if __name__ == '__main__':
    app.run(debug=True, port=8888)
