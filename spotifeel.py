from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    '''Return template index.html'''
    return render_template('index.html')
