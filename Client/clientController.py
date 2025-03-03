from flask import redirect, render_template, request, jsonify, url_for, session
import requests
from spotifeelApplication import user
from datetime import date
import emotionController

class clientController:
    '''
    Controller class handling client-side functionality for the Spotifeel application.
    Manages routing, authentication with Spotify, and emotion-based playlist generation.
    '''

    base_url : str = 'http://127.0.0.1:5000'

    @staticmethod
    def login_page():
        '''        
        Returns:
            Rendered login.html template
        '''

        return render_template('login.html')
    
    @staticmethod
    def oauth_spotify():
        '''
        Initiates Spotify OAuth authentication flow.
        
        Gets auth_url via the login() function in SpotifyApi class and
        redirects user to Spotify's login page.
        
        Returns:
            Redirect to Spotify authorization page
        '''

        auth_url = user.redirect_to_auth_code_flow()
        return redirect(auth_url)
    
    @staticmethod
    def login_callback():
        '''
        Handles the callback after Spotify authentication.
        
        The user is redirected to this endpoint after logging in to Spotify.
        Exchanges the received authorization code for an access token.
        
        Returns:
            Redirect to index page on success or error JSON on failure
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
        Handles the callback after Spotify authentication.
        
        The user is redirected to this endpoint after logging in to Spotify.
        Exchanges the received authorization code for an access token.
        
        Returns:
            Redirect to index page on success or error JSON on failure
        '''
        if not user.is_user_logged_in():
            print("ERROR: user is not logged in")
            return redirect('/login')

        else:
            try:
                status = user.get_user_information()
                print("status here")
                print(status)
            
                userPrompt = request.form.get('userPrompt')
                
                print("kommer vi hit?")
                response = requests.post(f'{clientController.base_url}/emotions/generate',
                                        json={'prompt': userPrompt},
                                        headers={'Content-Type': 'application/json'})
                    
            except Exception as e:
                print(f"Exception : {e}")


        # Only try to parse JSON if we get a successful response
        if response.status_code == 200:
            response_data = response.json()
            return redirect(url_for('verify', response=response_data))
        
        else:
            print(f"Error: API returned status code {response.status_code}")
            return redirect('/')
    
    @staticmethod
    def get_index():
        '''
        Renders the main chat interface.
        
        Verifies user authentication and renders the chat template with today's date.
        
        Returns:
            Rendered chat.html template or redirect to login page if user is not
                authenticated
        '''

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
        Confirms detected emotions with the user.
        
        Retrieves emotion data from the request, parses it, and presents
        options for the user to confirm or modify the detected emotions.
        
        Returns:
            Rendered verify.html template with emotion options or redirect
                to index if no emotion data is available
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
        Creates and displays a personalized Spotify playlist based on detected emotions.
        
        Checks user authentication, processes the user's emotion preference (stay with
        current feeling or choose opposite), generates song recommendations using the
        emotion API, and creates a Spotify playlist with those songs.
        
        Returns:
            Rendered playlist.html template with created playlist details or redirect to
                login page if user is not authenticated

        '''

        if not user.is_user_logged_in():
            print("ERROR: user is not logged in")
            return redirect ('/login')

        else:

            data = request.get_json()
            action = data.get("message")
            emotion = session.get('emotion')

            if action == "false":
                emotion = requests.get(f'{clientController.base_url}/emotions/{emotion}/opposite')
                emotion = emotion.json()
            #Create playlist, OPEN & Spotify work together
            today = date.today()
            user.get_user_information()
            songs_for_playlist = requests.post(f'{clientController.base_url}/song-recommendations/{emotion}',
                        headers={'Content-Type': 'application/json'})
            emotion = str(emotion)
            json_format = {'name' : 'name', 'tracks' : []}
            if songs_for_playlist.status_code == 200:
                response_data = songs_for_playlist.json()
                json_format = clientController.format_playlist(response_data, emotion)

            response = requests.post(f'{clientController.base_url}/playlists', 
                                headers = {
                                    'Authorization': 'Bearer ' + user.access_token,
                                    "Content-Type": "application/json"
                                },
                                json=json_format)

            response = response.json()
            new_playlist_id = response.get('playlist_id')
            song_info = response.get('tracks')
            display_feeling = emotion.capitalize() 
            return render_template('playlist.html', new_playlist_id=new_playlist_id, song_info=song_info, display_feeling=display_feeling, today=today)


    def format_playlist(tracks, emotion):
        '''
        Formats track data for playlist creation.
        
        Takes track information and emotion type to create a properly
        formatted playlist object for the Spotify API.
        
        Args:
            tracks (dict): Dictionary containing track information from the 
            recommendation API emotion (str): The emotion label for naming
            the playlist
            
        Returns:
            dict: Formatted playlist dictionary with name and tracks
        '''

        playlist = {'name' : f'{emotion}', 'tracks' : tracks['tracks']}
        return playlist



