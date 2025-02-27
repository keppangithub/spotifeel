import emotionAPI
def negated_feeling_id(id: int) -> str:
    '''
    Check which category the feeling received is a part of and return the opposite emotion.
    
    parameter:
    - id (int)
    
    returns:
    - a feeling (str)
    '''
    feelings = {
        "happy": [5, 6, 7],
        "angry": [1, 2],
        "sad": [3, 4, 8, 9, 10, 11, 12, 13]
    }
    
    if id in feelings["happy"]:
        return "sad"
    
    if id in feelings["angry"]:
        return "chill"
    
    if id in feelings["sad"]:
        return "happy"
    
    return "unknown"


def negated_feeling_str(feeling: str) -> str:
    '''
    Check which category the feeling received is a part of and return the oposit emotion.
    
    parameter:
    - a feeling (str)
    
    returns:
    - a feeling (str)
    '''
    feelings = {
        "happy": ["euphoric", "loving", "happy", "Euphoric", "Loving", "Happy"],
        "angry": ["urious", "frustrated", "Furious", "Frustrated"],
        "sad": ["horrified", "disappointed", "useless", "regretful", "dejected", "unhappy", "scared", "anxious", "Horrified", "Disappointed", "Useless", "Regretful", "Dejected", "Unhappy", "Dcared", "Anxious"]
    } 
    for category, feelings in feelings.items():
        if feeling in feelings:
            if category == "happy":
                return "sad"
            
            if category == "angry":
                return "chill"
            
            if category == "sad":
                return "happy"

def get_id(emotion : str) ->str:
   return emotionAPI.get_id_by_name(emotion)

def get_emotion(id: int) ->str:
    return emotionAPI.get_emotion_by_id_json(id)

def get_emotions():
    return emotionAPI.emotions_json