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
    return controller.login_page()

@app.route('/oauth_spotify')
def oauth_spotify():
    return controller.oauth_spotify()

@app.route('/callback')
def login_callback():
    return controller.login_callback()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return controller.post_index()
        
    else:
        return controller.get_index()

@app.route("/verify")
def verify():
    return controller.verify_emotion()


@app.route('/playlist', methods=['POST'])
def playlist():
    return controller.playlist()

'''
Starting server with port - 8888
'''
if __name__ == '__main__':
    app.run(debug=True, port=8888)
