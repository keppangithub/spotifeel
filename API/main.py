from flask import Flask, jsonify, request
import promptGPT
import emotionControllerAPI
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

app = Flask(__name__)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request", "message": str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found", "message": str(error)}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed", "message": "The method is not allowed for the requested URL"}), 405

@app.errorhandler(415)
def unsupported_media_type(error):
    return jsonify({"error": "Unsupported media type", "message": "Content-Type must be application/json"}), 415

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error", "message": "An unexpected error occurred"}), 500

def handle_exceptions(func):
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
    try:
        emotions = emotionControllerAPI.get_emotions()
        if not emotions:
            raise NotFound("No emotions found")
        return emotions
    except Exception as e:
        app.logger.error(f"Error fetching emotions: {str(e)}")
        raise

@app.route('/emotions/generate', methods=['POST'])
@handle_exceptions
def generate_emotion():
    if not request.is_json:
        return jsonify({"error": "Unsupported media type", "message": "Content-Type must be application/json"}), 415
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad request", "message": "Empty request body"}), 400
    
    if 'prompt' not in data:
        return jsonify({"error": "Missing parameter", "message": "Required parameter 'prompt' missing"}), 400
    
    prompt = str(data.get('prompt'))
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
    if not isinstance(id, int):
        return jsonify({"error": "Invalid parameter", "message": "Emotion ID must be an integer"}), 400
    
    if not (1 <= id <= 13):
        return jsonify({"error": "Invalid parameter", "message": "Emotion ID must be between 1 and 13"}), 400
    
    try:
        result = emotionControllerAPI.negated_feeling_id(id)
        if not result:
            return jsonify({"error": "Processing error", "message": f"Could not find opposite for emotion ID {id}"}), 422
        return result
    except Exception as e:
        app.logger.error(f"Error finding opposite emotion for ID {id}: {str(e)}")
        raise

@app.route('/song-recommendations/<int:id>', methods=['POST'])
@handle_exceptions
def create_playlist_by_id(id):
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

@app.route('/song-recommendations/<string:emotion>', methods=['POST'])
@handle_exceptions
def create_playlist_by_emotion(emotion):
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)