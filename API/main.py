from flask import Flask, jsonify, request
import promptGPT
import emotionControllerAPI
import playlist_API as playlist_tmp
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

app = Flask(__name__)

@app.errorhandler(400)
def bad_request(error):
    '''
    Handle 400 Bad Request errors.

    Args:
        error (Exception): The error object containing details of the bad request.

    Returns:
        tuple: A JSON response containing the error message and details, along with the HTTP status code 400.
    '''
    return jsonify({"error": "Bad request", "message": str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    '''
    Handle 404 Not Found errors.

    Args:
        error (Exception): The error object containing details of the resource not found.

    Returns:
        tuple: A JSON response containing the error message and details, along with the HTTP status code 404.
    '''
    return jsonify({"error": "Resource not found", "message": str(error)}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    '''
    Handle 405 Method Not Allowed errors.

    Args:
        error (Exception): The error object containing details of the method not allowed.

    Returns:
        tuple: A JSON response containing the error message and details, along with the HTTP status code 405.
    '''
    return jsonify({"error": "Method not allowed", "message": "The method is not allowed for the requested URL"}), 405

@app.errorhandler(415)
def unsupported_media_type(error):
    '''
    Handle 415 Unsupported Media Type errors.

    Args:
        error (Exception): The error object containing details of the unsupported media type.

    Returns:
        tuple: A JSON response containing the error message and details, along with the HTTP status code 415.
    '''
    return jsonify({"error": "Unsupported media type", "message": "Content-Type must be application/json"}), 415

@app.errorhandler(500)
def internal_server_error(error):
    '''
    Handle 500 Internal Server errors.

    Args:
        error (Exception): The error object containing details of the internal server error.

    Returns:
        tuple: A JSON response containing the error message and details, along with the HTTP status code 500.
    '''
    return jsonify({"error": "Internal server error", "message": "An unexpected error occurred"}), 500

def handle_exceptions(func):
    '''
    A decorator to handle specific exceptions in a Flask view function.

    Args:
        func (function): The view function to wrap with exception handling.

    Returns:
        function: The wrapped function with exception handling in a JSON format.
    
    Exceptions Handled:
        - KeyError: Returns a 400 response indicating a missing parameter.
        - ValueError: Returns a 400 response indicating an invalid value.
        - NotFound: Returns a 404 response indicating the resource was not found.
        - Exception: Catches any other unexpected errors and returns a 500 response.
    '''
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except KeyError as e:
            return jsonify({"error": "Missing parameter", "message": f"Required parameter missing: {str(e)}"}), 400
        
        except ValueError as e:
            return jsonify({"error": "Invalid value", "message": str(e)}), 400
        
        except NotFound as e:
            return jsonify({"error": "Not found", "message": str(e)}), 404
        
        except Exception as e:
            app.logger.error(f"Unexpected error: {str(e)}")
            
            return jsonify({"error": "Server error", "message": "An unexpected error occurred"}), 500
        
    wrapper.__name__ = func.__name__
    
    return wrapper

@app.route('/emotions', methods=['GET'])
@handle_exceptions
def get_emotions():
    '''
    API endpoint - GET.
    Retrieve the list of emotions.

    Returns:
        Response: A JSON response containing the list of emotions if successful, or an error message if any issues arise.
    
    Raises:
        NotFound: If no emotions are found in the data source.
        Exception: For any other errors that may occur during the retrieval process.
    '''
    try:
        emotions = emotionControllerAPI.get_emotions()
        
        if not emotions:
            raise NotFound("No emotions found")
        
        return emotions
    
    except Exception as e:
        app.logger.error(f"Error fetching emotions: {str(e)}")
        raise

@app.route('/recommend/emotion', methods=['GET'])
@handle_exceptions
def generate_emotion():
    '''
    API endpoint - GET.
    Generate an emotion based on a user-provided prompt.

    Returns:
        Response: A JSON response with the generated emotion or an error message, with the corresponding HTTP status code.

    Error Handling:
        - 415: Unsupported Media Type if the Content-Type is not application/json.
        - 422: Unprocessable Entity if the prompt cannot generate a valid emotion.
    '''
    if not request.is_json:
        return jsonify({"error": "Unsupported media type", "message": "Content-Type must be application/json"}), 415
    
    prompt = request.args.get('prompt')
    print(f'prompt: {prompt}')
    
    if not prompt.strip():
        return jsonify({"error": "Invalid value", "message": "Prompt cannot be empty"}), 400
    
    try:
        result = promptGPT.run_prompt(prompt)
        
        if not result:
            return jsonify({"error": "Processing error", "message": "Could not generate emotion from prompt"}), 422
        
        return jsonify(result)
    
    except Exception as e:
        app.logger.error(f"Error generating emotion: {str(e)}")
        raise

@app.route('/emotions/<int:id>', methods=['GET'])
@handle_exceptions
def get_emotion_by_id(id):
    '''
    API endpoint - GET.
    Retrieve an emotion by its ID.

    Args:
        id (int): An emotion ID.

    Returns:
        Response: A JSON response containing the requested emotion or an error message, along with the appropriate HTTP status code.

    Error Handling:
        - 400: Invalid parameter if the ID is not an integer or not between 1 and 13.
        - 404: Not Found if the emotion with the given ID is not found.
    '''
    if not isinstance(id, int):
        return jsonify({"error": "Invalid parameter", "message": "Emotion ID must be an integer"}), 400
    
    if not (1 <= id <= 13):
        return jsonify({"error": "Invalid parameter", "message": "Emotion ID must be between 1 and 13"}), 400

    try:
        emotion = emotionControllerAPI.get_emotion(id)
        
        if not emotion:
            raise NotFound(f"Emotion with ID {id} not found")
        
        return emotion
    
    except Exception as e:
        app.logger.error(f"Error fetching emotion {id}: {str(e)}")
        raise

@app.route('/emotions/<string:emotion>', methods=['GET'])
@handle_exceptions
def get_emotion_by_str(emotion):
    '''
    API endpoint - GET.
    Retrieve the ID of an emotion by its name.

    Args:
        emotion (str): an emotion name.

    Returns:
        Response: A JSON response containing the emotion ID or an error message, along with the appropriate HTTP status code.

    Error Handling:
        - 400: Invalid parameter if the emotion name is empty or only whitespace.
        - 404: Not Found if the emotion with the given name is not found.
    '''
    if not emotion or not emotion.strip():
        return jsonify({"error": "Invalid parameter", "message": "Emotion name cannot be empty"}), 400
    
    try:
        result = emotionControllerAPI.get_id(emotion)
        
        if not result:
            raise NotFound(f"Emotion '{emotion}' not found")
        
        return result
    
    except Exception as e:
        app.logger.error(f"Error fetching emotion '{emotion}': {str(e)}")
        raise

@app.route('/emotions/<int:id>/opposite', methods=['GET'])
@handle_exceptions
def get_opposite_emotion(id):
    '''
    API endpoint - GET.
    Retrieve the opposite (negated) emotion based on its ID.

    Args:
        id (int): en emotion ID.

    Returns:
        Response: A JSON response containing the negated emotion if successful, or an error message, along with the appropriate HTTP status code.

    Error Handling:
        - 400: Invalid parameter if the emotion ID is not between 1 and 13.
        - 422: Processing error if the opposite emotion for the given ID could not be found.
    '''
    if not (1 <= id <= 13):
        return jsonify({"error": "Invalid parameter", "message": "Emotion ID must be between 1 and 13"}), 400
    
    try:
        result = emotionControllerAPI.negated_feeling_id(id)
        
        if not result:
            return jsonify({"error": "Processing error", "message": f"Could not find opposite for emotion ID {id}"}), 422
        
        return jsonify(result)
    
    except Exception as e:
        app.logger.error(f"Error finding opposite emotion for ID {id}: {str(e)}")
        raise

@app.route('/emotions/<string:emotion>/opposite', methods=['GET'])
@handle_exceptions
def get_opposite_emotion_by(emotion): 
    '''
    API endpoint - GET.
    Retrieve the opposite (negated) emotion based on its name.

    Args:
        emotion (str): an emotion name.

    Returns:
        Response: A JSON response containing the negated emotion if successful, or an error message, along with the appropriate HTTP status code.

    Error Handling:
        - 422: Processing error if the opposite emotion for the given name could not be found.
    '''
       
    try:
        result = emotionControllerAPI.negated_feeling_str(emotion)
        
        if not result:
            return jsonify({"error": "Processing error", "message": f"Could not find opposite for emotion {emotion}"}), 422
        
        return jsonify(result)
    
    except Exception as e:
        app.logger.error(f"Error finding opposite emotion for ID {id}: {str(e)}")
        raise

@app.route('/recommend/songs/<int:id>', methods=['GET'])
@handle_exceptions
def create_playlist_by_id(id):
    '''
    API endpoint - GET.
    Get song recommendations from Open AI's API  based on an emotion ID.

    Args:
        id (int): An emotion ID.

    Returns:
        Response: A JSON response containing the created playlist or an error message, along with the appropriate HTTP status code.

    Error Handling:
        - 400: Invalid parameter if the emotion ID is not an integer or not between 1 and 13.
        - 422: Processing error if the playlist cannot be created for the given emotion ID.
    '''
    if not isinstance(id, int):
        return jsonify({"error": "Invalid parameter", "message": "Emotion ID must be an integer"}), 400
    
    if not (1 <= id <= 13):
        return jsonify({"error": "Invalid parameter", "message": "Emotion ID must be between 1 and 13"}), 400
    
    try:
        result = promptGPT.create_playlist(id)
        
        if not result:
            return jsonify({"error": "Processing error", "message": f"Could not create playlist for emotion ID {id}"}), 422
        
        return result
    
    except Exception as e:
        app.logger.error(f"Error creating playlist for ID {id}: {str(e)}")
        raise

@app.route('/recommend/songs/<string:emotion>', methods=['GET'])
@handle_exceptions
def create_playlist_by_emotion(emotion):
    '''
    API endpoint - POST.
    Get song recommendations from Open AI's API based on an emotion name.

    Args:
        emotion (str): an emotion name.

    Returns:
        Response: A JSON response containing the created playlist or an error message, along with the appropriate HTTP status code.

    Error Handling:
        - 400: Invalid parameter if the emotion name is empty or only whitespace.
        - 422: Processing error if the playlist cannot be created for the given emotion name.
    '''
    if not emotion or not emotion.strip():
        return jsonify({"error": "Invalid parameter", "message": "Emotion name cannot be empty"}), 400
    
    try:
        result = promptGPT.create_playlist(emotion)
        
        if not result:
            return jsonify({"error": "Processing error", "message": f"Could not create playlist for emotion '{emotion}'"}), 422
        
        return result
    
    except Exception as e:
        app.logger.error(f"Error creating playlist for emotion '{emotion}': {str(e)}")
        raise

@app.route('/playlists/<int:id>', methods=['GET'])
def get_playlists_id(id):
    '''
    API endpoint - GET.
    Retrieve a created playlist based on its id. 
    
    Args:
        id (int): a playlist id.
        
    Returns:
        Response: A JSON response containing the requested playlist if successful, or an error message with the appropriate HTTP status code.

    '''
    return playlist_tmp.get_playlist_id(int(id))

@app.route('/playlists', methods=['GET'])
def get_playlists():
    '''
    API endpoint - GET.
    Retrieve all playlists that have been created and loaded into the system.
    
    Returns:
        Response: A JSON response containing the list of loaded playlists if successful, or an error message with the appropriate HTTP status code.
    '''
    return playlist_tmp.get_playlist()


@app.route('/playlists', methods=['POST'])
def post_playlists():
    '''
    API endpoint - POST.
    Create a playlist.

    Returns:
        Response: A JSON response containing either the created playlist or an error message with the appropriate HTTP status code.

    Error Handling:
        - 401: If the authorization header is missing or invalid.
        - 400: If the request is not in JSON format or if the playlist data is invalid.
        - 500: If an unexpected error occurs during the request processing.
    '''
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Missing or invalid authorization token"}), 401
    
    access_token = auth_header.split(' ')[1]
    
    try:
        json_data = request.get_json(force=True)
        
        if not json_data:
            return jsonify({"error": "Request must be Json"}), 400
        
        validate_data = playlist_tmp.validate_playlist_json(json_data)
        
        if validate_data is True:
            return playlist_tmp.post_playlist(access_token, json_data), 201
        
        else:
            return jsonify({"error": validate_data}), 400
        
    except Exception as e:
        return jsonify({"error": "Unexpected error"}), 500

# Start the server which hosts the API
if __name__ == '__main__':
    app.run(debug=True, port=5000)