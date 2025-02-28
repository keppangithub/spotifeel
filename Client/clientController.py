from flask import redirect, render_template, request, jsonify, url_for, session
import requests
from spotifeelApplication import user
from datetime import date
import emotionController

class clientController:
    @staticmethod
    def login_page():
        '''Return template login.html'''
        return render_template('login.html')
    
    @staticmethod
    def oauth_spotify():
        '''
        Get auth_url via the login() function in the class SpotifyApi

        Redirect user to the login Spotify's login via Spotify API

        '''
        auth_url = user.redirectToAuthCodeFlow()
        return redirect(auth_url)
    
    @staticmethod
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
        
    @staticmethod
    def post_index():
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
            userPrompt = request.form.get('userPrompt')
            print(userPrompt)

        response = requests.post('http://127.0.0.1:5000/emotions/generate',
                        json={'prompt': userPrompt},
                        headers={'Content-Type': 'application/json'})

        # Print the raw response before parsing as JSON
        print("Status code:", response.status_code)
        print("Raw response:", response.text)

        # Only try to parse JSON if we get a successful response
        if response.status_code == 200:
            response_data = response.json()
            print(response_data)
            return redirect(url_for('verify', response=response_data))
        else:
            print(f"Error: API returned status code {response.status_code}")
    
    @staticmethod
    def get_index():
        if not user.is_user_logged_in():
            print("ERROR: user is not logged in")
            return redirect ('/login')

        else:
            user.get_user_information()
            today = date.today()
            return render_template('chat.html', today=today)
        
    @staticmethod
    def verify_emotion():
        '''
        returns:
        - verify.html
        '''
        response = request.args.get('response', None)

        if response is None:
            return redirect(url_for('index'))
        
        response = str(response)
        emotion = emotionController.get_emotions(response)
        session['emotion'] = response

        if len(emotion) == 3:
            title, button1, button2 = emotion

        else:
            title, button1, button2 = "Error", "Invalid", "Response"

        return render_template('verify.html', title=title, button1=button1, button2=button2)
    
    @staticmethod
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
            emotion = session.get('emotion')

            if action == "false":
                emotion = requests.post(f'http://127.0.0.1:5000/emotions/{emotion}/opposite')
                emotion = emotion.json()
            #Create playlist, OPEN & Spotify work together
            today = date.today()
            user.get_user_information()
            songs_for_playlist = requests.post(f'http://127.0.0.1:5000/song-recommendations/{emotion}',
                        headers={'Content-Type': 'application/json'})
            if songs_for_playlist.status_code == 200:
                response_data = songs_for_playlist.json()
                print("Response data")
                print(response_data)

            emotion = str(emotion)

            new_playlist_id = user.create_new_playlist(user.user_id, f'{emotion.capitalize()} - {today}')
            song_info = user.add_to_playlist(new_playlist_id, response_data)
            display_feeling = emotion.capitalize()
            
            return render_template('playlist.html', new_playlist_id=new_playlist_id, song_info=song_info, display_feeling=display_feeling, today=today)
        
