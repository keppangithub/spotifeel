# Eftersom denna fil ligger i API-mappen
from flask import Flask, jsonify, request
# Importera moduler från samma mapp (API)
import promptGPT
import emotionControllerAPI
# Om denna import inte fungerar, använd:
# from . import promptGPT, spotifeelAPI

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)


    '''Lägg till alla felkoder för alla endpoints'''