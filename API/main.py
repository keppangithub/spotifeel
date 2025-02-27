from flask import Flask, jsonify, request
import promptGPT
import emotionControllerAPI
import spotifeelAPI as spotifeel
import playlist_API as playlist_tmp

app = Flask(__name__)

@app.route('/emotions', methods=['GET'])
def get_emotions():
    data = None
    prompt = None
    try:
        data = request.get_json()
        if data:
            try:
                prompt = str(data.get('prompt'))
            except Exception as e:
                print(f"Error: {e}")

    except Exception as e:
        print(f"Error: {e}")

    if data is None:
        return emotionControllerAPI.get_emotions()

    if prompt is not None:
        return jsonify(promptGPT.run_prompt(prompt))

@app.route('/emotions/<int:id>', methods=['GET'])
def get_emotion_by_id(id):
    emotion_id = id
    
    if not (1 <= emotion_id <= 13):
        return jsonify({"error": "Invalid emotion ID"}), 400

    return emotionControllerAPI.get_emotion(id)

@app.route('/emotions/<string:emotion>', methods=['GET'])
def get_emotion_by_str(emotion):
    return emotionControllerAPI.get_id(emotion)

@app.route('/emotions/<int:id>/opposite', methods=['GET'])
def get_opposite_emotion(id):
    if not (1 <= id <= 13):
        return jsonify({"error": "Invalid emotion ID"}), 400
        
    return emotionControllerAPI.negated_feeling_id(id)



@app.route('/playlists/<int:id>', methods=['GET'])
def get_playlists_id(id):
    
    return playlist_tmp.get_playlist_id(int(id))

@app.route('/playlists', methods=['GET'])
def get_playlists():
    return playlist_tmp.get_playlist()


@app.route('/playlists', methods=['POST'])
def post_playlists():
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
            return jsonify({playlist_tmp.post_playlist(access_token, json_data)}), 201
        else:
            return jsonify({"error": validate_data}), 400
        
    except Exception as e:
        return jsonify({"error": "Unexpected error"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)


    '''Lägg till alla felkoder för alla endpoints'''