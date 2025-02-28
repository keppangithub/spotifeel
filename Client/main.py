from flask import Flask, redirect, render_template, request, jsonify, url_for, session
from datetime import date
from app import app, user
from flask_swagger_ui import get_swaggerui_blueprint
import os

from application import app, controller
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


@app.route('/playlist', methods=['POST'])
def playlist():
    return controller.playlist()

'''
Starting server with port - 8888
'''
if __name__ == '__main__':
    app.run(debug=True, port=8888)
