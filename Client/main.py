from flask import request
from flask_swagger_ui import get_swaggerui_blueprint

from app import app
from clientController import clientController
from flask_swagger_ui import get_swaggerui_blueprint
import emotionController

controller = clientController()

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
    '''
    Route to display the login page.
    
    Returns:
        Rendered login page template
    '''
    return controller.login_page()

@app.route('/oauth_spotify')
def oauth_spotify():
    '''
    Route to initiate Spotify OAuth authentication flow.
        
    Returns:
        Redirect to Spotify's authorization page.
    '''
    return controller.oauth_spotify()

@app.route('/callback')
def login_callback():
    '''
    Callback route for Spotify OAuth authentication.
    '''
    return controller.login_callback()

@app.route('/', methods=['POST', 'GET'])
def index():
    '''
    Main application route that handles both GET and POST requests.
    
    GET: Displays the main chat interface
    POST: Processes user diary input for emotion analysis
    
    Returns:
        For GET - rendered chat template
        For POST - redirect to verification page with emotion data
    '''
    if request.method == 'POST':
        return controller.post_index()
        
    else:
        return controller.get_index()

@app.route("/verify")
def verify():
    '''
    Route to verify detected emotions.
    
    Displays the detected emotions and allows the user to confirm
    or choose different emotions for playlist generation.
    
    Returns:
        Rendered verification page with emotion options
    '''
    return controller.verify_emotion()


@app.route('/playlist', methods=['POST'])
def playlist():
    '''
    Route to generate and display a Spotify playlist based on emotions.
    
    Processes the user's emotion preference, generates song recommendations,
    and creates a playlist on the user's Spotify account.
    
    Returns:
        Rendered playlist page with created playlist details
    '''
    return controller.playlist()

'''
Starting server with port - 8888
'''
if __name__ == '__main__':
    app.run(debug=True, port=8888)