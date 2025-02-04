from flask import Flask, redirect, render_template, request, jsonify, url_for, session
from datetime import date
import promptGPT, feelings, spotifeelAPI, playlists
from app import app, user
from flask_swagger_ui import get_swaggerui_blueprint
import os
import requests

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
        '''
                 today = date.today()
        user.get_user_information()
        songs_for_playlist = promptGPT.create_playlist(feeling)
        new_playlist_id = user.create_new_playlist(user.user_id, f'{feeling.capitalize()} - {today}')
        song_info = user.add_to_playlist(new_playlist_id, songs_for_playlist)
        display_feeling = feeling.capitalize()


        playlists.add_to_playlist(new_playlist_id)
          '''


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
def get_all_emotions():
    '''
    Gets all available emotions from the API.

    Returns:
    - JSON response of all emotions.
    '''
    return jsonify(spotifeelAPI.get_emotions())

@app.route('/emotions/<int:emotionId>', methods=['GET'])
def get_emotion_by_id(emotionId):
    '''
    Gets a specific emotion by its ID from the API.

    Parameters:
    - emotionId (int): The ID of the desired emotion.

    Returns:
    - JSON response containing the emotion with the specified ID.
    '''
    return jsonify(spotifeelAPI.get_emotion_by_id(f'{emotionId}'))


@app.route('/playlists', methods=['GET'])
def get_playlists():

    json_data = None;
    try:
        json_data = request.get_json()
        playlist_id = int(json_data['playlist_id'])
    except Exception as e:
        print(f"Error: {e}")

    if json_data is None:
        return jsonify(spotifeelAPI.get_playlists()), 201
    else:
        playlist = spotifeelAPI.get_playlists()
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
    user.set_acces_token(access_token)
    print(f"{session}")

    try:
        json_data = request.get_json(force=True)
        print(json_data)
        
        if not json_data:
            return jsonify({"error": "Request must be Json"}), 400
        
        if not "emotion_id" in json_data or not isinstance(json_data["emotion_id"], int) or not (1 <= json_data["emotion_id"] <= 13):
            return jsonify({"error": "'number' is required and must be an integer between 1 and 13"}), 400


        emotionId = int(json_data["emotion_id"])
        feeling = spotifeelAPI.get_emotion_by_id(emotionId)
        today = date.today()
        user.get_user_information()
        songs_for_playlist = promptGPT.create_playlist(feeling)
        new_playlist_id = user.create_new_playlist(user.user_id, f'{feeling.capitalize()} - {today}')  
        user.add_to_playlist(new_playlist_id, songs_for_playlist)

        playlist = user.get_user_playlist(new_playlist_id)

        formatted_playlist = {
            "name": playlist["name"],
            "uri": playlist["uri"],
            "songs": []
        }

        for item in playlist["tracks"]["items"]:
            formatted_song = {
                "name": item["track"]["name"],
                "artist": ', '.join(artist["name"] for artist in item["track"]["artists"]),
                "uri": item["track"]["uri"]
            }
            formatted_playlist["songs"].append(formatted_song)

        print(jsonify(formatted_playlist))

        return jsonify(formatted_playlist), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


'''
Starting server with port - 8888
'''
if __name__ == '__main__':
    app.run(debug=True, port=8888)
