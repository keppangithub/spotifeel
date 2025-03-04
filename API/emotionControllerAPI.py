import emotionAPI
def negated_feeling_id(emotion_id: int) -> str:
    '''
    Check which category the emotion received is a part of, and return the opposite emotion.
    
    Args:
        id (int): an emotion id
    
    Returns:
        str: an emotion or 'unknown' (if the emotion is not found).
    '''
    emotions = {
        "happy": [5, 6, 7],
        "angry": [1, 2],
        "sad": [3, 4, 8, 9, 10, 11, 12, 13]
    }
    
    if emotion_id in emotions["happy"]:
        return emotionAPI.get_emotion_by_id_json(11)
    
    if emotion_id in emotions["angry"]:
        return emotionAPI.get_emotion_by_id_json(6)
    
    if emotion_id in emotions["sad"]:
        return emotionAPI.get_emotion_by_id_json(7)
    
    return "unknown"


def negated_feeling_str(emotion: str) -> str:
    '''
    Check which category the emotion received is a part of, and return the opposit emotion.
    
    Args:
        emotion (str): an emotion name
    
    Returns:
        str: an emotion name or 'unknown' (if the emotion is not found).
    '''
    emotions = {
        "happy": ["euphoric", "loving", "happy", "Euphoric", "Loving", "Happy"],
        "angry": ["furious", "frustrated", "Furious", "Frustrated"],
        "sad": ["horrified", "disappointed", "useless", "regretful", "dejected", "unhappy", "scared", "anxious", "Horrified", "Disappointed", "Useless", "Regretful", "Dejected", "Unhappy", "Scared", "Anxious"]
    } 
    for category, emotions in emotions.items():
        if emotion in emotions:
            if category == "happy":
                return emotionAPI.get_emotion_by_id_json(11)
            
            if category == "angry":
                return emotionAPI.get_emotion_by_id_json(6)
            
            if category == "sad":
                return emotionAPI.get_emotion_by_id_json(7)
            
    return "unknown"

def get_id(emotion : str) -> str:
    '''
    Retrieve an emotion id based on a recieved emotion name.
    
    Args:
        emotion (str): an emotion name
    
    Returns:
        str: A JSON formated string containing either an id or an Error message (if the id is not found).
    '''
    return emotionAPI.get_id_by_name(emotion)

def get_emotion(emotion_id: int) -> str:
    '''
    Retrieve an emotion name based on a recieved emotion id.
    
    Args:
        emotion_id (int): an emotion id
    
    Returns:
        str: A JSON formated string containing either a name or an Error message (if the name is not found).
    '''
    return emotionAPI.get_emotion_by_id_json(emotion_id)

def get_emotions():
    '''
    Retrieve the list of emotions in JSON format.
    
    Returns:
        str: A JSON string representing the list of emotions.
    '''
    return emotionAPI.emotions_json

def get_regular_emotion(emotion_id: int) -> str:
    '''
    Retrieve an emotion based on its ID from the list of emotions. 

    Args:
        emotion_id (int): an emotion ID.
    
    Returns:
        str: the name of the emotion or an error message (if the emotion was not found).

    '''

    for emotion in emotionAPI.emotions:
        if emotion.id == id:
            return emotion.name
        
    return 'Invalid emotion'
    return emotionAPI.get_emotion_by_id(emotion_id)