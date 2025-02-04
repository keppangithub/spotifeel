from flask import Flask, jsonify, redirect, request, url_for, render_template, session
import yaml, playlists, os, json, promptGPT
from app import app

# Dictionary of emotions mapped to their respective IDs
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

# Set file paths for YAML and JSON API documentation files
yaml_file_path = os.path.join(os.getcwd(), 'static', 'swagger.yaml')
json_file_path = os.path.join(os.getcwd(), 'static', 'swagger.json')

# Read the YAML file containing API documentation
with open(yaml_file_path, 'r') as yaml_file:
    SWAGGER_SPEC = yaml.safe_load(yaml_file)

# Write the API documentation to a JSON file for serving as static content
with open(json_file_path, 'w') as json_file:
    json.dump(SWAGGER_SPEC, json_file, indent=2)


'''Routing for API documentation'''
@app.route('/docs/static/swagger.json')
def swagger_json():
    """
    Route to serve the API documentation in JSON format.

    Returns:
        JSON: The API documentation as a JSON response.
    """
    return jsonify(SWAGGER_SPEC)



def get_emotion_by_id(emotion_id):
    '''
   Retrieves a specific emotion based on its ID.

    Args:
        emotionId (str): The ID of the emotion to retrieve.

    Returns:
        str: The emotion corresponding to the provided ID.
    '''
    
    return emotions.get(str(emotion_id))


def get_emotions():
    '''
    Retrieves the complete dictionary of emotions.

    Returns:
        dict: A dictionary containing all emotions with their IDs as keys.
    '''
    return emotions

def get_playlists():
    return playlists.get_playlists()

def get_playlists_by_id(id):
    return playlists.get_playlists_by_id(id)
