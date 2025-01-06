from flask import Flask, redirect, render_template, request, jsonify, url_for, session
from spotifyAPI import SpotifyAPI
import promptGPT
import feelings

app = Flask(__name__)
app.secret_key = 'enhemlignyckel'
user = SpotifyAPI()


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

@app.route('/', methods=['POST', 'GET'])
def index():
    if not user.is_user_logged_in():
        print("ERROR: user is not logged in")
        return redirect ('/login')
    
    else:
        user.get_user_information()
        if request.method == 'POST':
            userPrompt = request.form.get('userPrompt')
            response = promptGPT.run_prompt(userPrompt)
            return redirect(url_for('verify', response=response))
        return render_template('chat.html')
    
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

    playlist = promptGPT.create_playlist(feeling)

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
    app.run(debug=True, port=8888)
    