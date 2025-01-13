from flask import Flask, redirect, render_template, request, jsonify, url_for, session
from datetime import date
import promptGPT, feelings, spotifeelAPI, playlists
from app import app, user
from flask_swagger_ui import get_swaggerui_blueprint

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
        user.add_to_playlist(new_playlist_id, songs_for_playlist)
        display_feeling = feeling.capitalize()
        
        playlists.add_to_playlist(new_playlist_id)
            
        return render_template('playlist.html', songs_for_playlist=songs_for_playlist, display_feeling=display_feeling, today=today)






@app.route('/feelings', methods=['GET'])
def get_all_emotions():
    '''
    Gets all available emotions from the API.

    Returns:
    - JSON response of all emotions.
    '''
    return jsonify(spotifeelAPI.get_emotions())

@app.route('/feelings/<int:emotionId>', methods=['GET'])
def get_emotion_by_id(emotionId):
    '''
    Gets a specific emotion by its ID from the API.

    Parameters:
    - emotionId (int): The ID of the desired emotion.

    Returns:
    - JSON response containing the emotion with the specified ID.
    '''
    return jsonify(spotifeelAPI.get_emotion_by_id(f'{emotionId}'))

@app.route('/playlists/<int:emotionId>', methods=['POST', 'GET'])
def post_playlist(emotionId):
    '''
    Creates a playlist based on a specific emotion and adds it to the user's Spotify account.

    - Checks if the user is logged in; if not, redirects to the login page.
    - Retrieves the emotion associated with the given ID.
    - Uses GPT to generate a playlist based on the emotion.
    - Creates and saves the playlist in the user's Spotify account.
    - Formats the playlist for API response.

    Parameters:
    - emotionId (int): The ID of the emotion to create the playlist for.

    Returns:
    - Redirect to login page if the user is not logged in.
    - JSON response containing the formatted playlist.
    '''
    if 'user_token' not in session:
        print("ERROR: user is not logged in")
        return redirect('/login')

    feeling = spotifeelAPI.get_emotion_by_id(f'{emotionId}')

    today = date.today()
    user.get_user_information()
    songs_for_playlist = promptGPT.create_playlist(feeling)
    new_playlist_id = user.create_new_playlist(user.user_id, f'{feeling.capitalize()} - {today}')  # Skapa ny playlist
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

    return jsonify(formatted_playlist)


@app.route('/playlists', methods=['GET'])
def get_all_playlists():
    return jsonify("spotifeelAPI.get_playlists()")

@app.route('/playlists/<int:id>', methods=['GET'])
def get_playlist_by_id(playlist_id):
    return jsonify("spotifeelAPI.get_platlists_by_id(f'{playlist_id}')")

'''
Starting server with port - 8888
'''
if __name__ == '__main__':
    app.run(debug=True, port=8888)
