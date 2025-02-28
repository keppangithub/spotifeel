from flask import Flask

def create_app():
    '''Initialize the Flask application'''
    app = Flask(__name__)
    app.secret_key = 'enhemlignyckel'
    return app

app = create_app()