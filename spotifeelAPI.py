from flask import Flask, jsonify, redirect, request, url_for, render_template, session
import yaml
import os
import json
import promptGPT
from app import app

emotions = {
        "1": "Furious",
        "2": "Frustrated",
        "3": "Horrified",
        "4": "Disappointed",
        "5": "Euphoric",
        "6": "Loving",
        "7": "Happy",
        "8": "Useless",
        "9": "Regretful",
        "10": "Dejected",
        "11": "Unhappy",
        "12": "Scared",
        "13": "Anxious"
    }

'''Sets the file paths for the YAML and JSON file'''
yaml_file_path = os.path.join(os.getcwd(), 'static', 'swagger.yaml')
json_file_path = os.path.join(os.getcwd(), 'static', 'swagger.json')

'''Reads the Yaml file for API documentation'''
with open(yaml_file_path, 'r') as yaml_file:
    SWAGGER_SPEC = yaml.safe_load(yaml_file)
'''Writes the API documentation to a JSON file'''
with open(json_file_path, 'w') as json_file:
    json.dump(SWAGGER_SPEC, json_file, indent=2)


'''Routing for API documentation'''
@app.route('/static/swagger.json')
def swagger_json():
    return jsonify(SWAGGER_SPEC)

'''Returns a given emotion based on its ID'''
def getEmotionById(emotionId):
    return emotions[emotionId]

def getEmotions():
    return emotions
