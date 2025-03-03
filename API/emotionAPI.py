import json

class Emotion:
    def __init__(self, id: int, name: str) -> None:
        '''
        Initialize a new instance of the Emotion class.

        Attributes:
            id (int): an emotion id
            name (str): an emotion name

        Returns:
            void
        '''
        self.id = id
        self.name = name
    
    def to_dict(self) -> dict:
        '''
        Convert the object attributes to a dictionary.

        Returns:
            dict: A dictionary containing the 'id' and 'name' attributes of the object.
        '''
        return {"id": self.id, "name": self.name}

emotions = [
    Emotion(1, "Furious"),
    Emotion(2, "Frustrated"),
    Emotion(3, "Horrified"),
    Emotion(4, "Disappointed"),
    Emotion(5, "Euphoric"),
    Emotion(6, "Loving"),
    Emotion(7, "Happy"),
    Emotion(8, "Useless"),
    Emotion(9, "Regretful"),
    Emotion(10, "Dejected"),
    Emotion(11, "Unhappy"),
    Emotion(12, "Scared"),
    Emotion(13, "Anxious")
]

emotions_json = json.dumps([e.to_dict() for e in emotions], indent=10)

# Flytta metoderna ut från Emotion-klassen så de blir modulnivå-funktioner
def get_id_by_name(name: str) -> str:
    '''
    Retrieve the ID of an emotion based on its name from the list of emotions. 
    
    Args:
        name (str): an emotion name

    Returns:
        str: A JSON formated string containing either an id or an Error message (if the id is not found).
    '''
    for emotion in emotions:
        if emotion.name.lower() == name.lower():
            return json.dumps({"id": emotion.id})
        
    return json.dumps({"error": "Emotion not found"})

def get_emotion_by_id_json(emotion_id: int) -> str:
    '''
    Retrieve an emotion based on its ID from the list of emotions. 
    
    Args:
        emotion_id (int): an emotion id

    Returns:
        Str: A JSON formated string containing either a name or an Error message (if the name is not found).
    '''
    for emotion in emotions:
        if emotion.id == emotion_id:
            return json.dumps(emotion.to_dict())
        
    return json.dumps({"error": "Emotion not found"})

def get_emotion_by_id(id: int) -> str:
    '''
    Retrieve an emotion based on its ID from the list of emotions. 
    
    Args:
        emotion_id(int): an emotion id
    
    Returns:
        str: the name of the emotion or an error message (if the emotion was not found).
    '''
    for emotion in emotions:
        if emotion.id == id:
            return emotion.name
        
    return 'Invalid emotion'

def negated_feeling_id(emotion_id: int) -> str:
    '''
    Check which category the emotion received is a part of, and return the opposite emotion.
    
    Args:
        id (int): an emotion id
    
    Returns:
        str: an emotion or 'unknown' (if the emotion is not found).
    '''
    emotions_categories = {
        "happy": [5, 6, 7],
        "angry": [1, 2],
        "sad": [3, 4, 8, 9, 10, 11, 12, 13]
    }
    
    if emotion_id in emotions_categories["happy"]:
        return "sad"
    
    if emotion_id in emotions_categories["angry"]:
        return "chill"
    
    if emotion_id in emotions_categories["sad"]:
        return "happy"
    
    return "unknown"

def negated_feeling_str(emotion: str) -> str:
    '''
    Check which category the emotion received is a part of, and return the opposit emotion.
    
    Args:
        emotion (str): an emotion name
    
    Returns:
        str: an emotion name or 'unknown' (if the emotion is not found).
    '''
    emotions_categories = {
        "happy": ["euphoric", "loving", "happy", "Euphoric", "Loving", "Happy"],
        "angry": ["furious", "frustrated", "Furious", "Frustrated"],
        "sad": ["horrified", "disappointed", "useless", "regretful", "dejected", "unhappy", "scared", "anxious", "Horrified", "Disappointed", "Useless", "Regretful", "Dejected", "Unhappy", "Scared", "Anxious"]
    } 
    
    for category, emotion_list in emotions_categories.items():
        if emotion in emotion_list:
            if category == "happy":
                return "sad"
            
            if category == "angry":
                return "chill"
            
            if category == "sad":
                return "happy"
    
    return "unknown"

def get_id(emotion: str) -> str:
    '''
    Retrieve an emotion id based on a recieved emotion name.
    
    Args:
        emotion (str): an emotion name
    
    Returns:
        str: A JSON formated string containing either an id or an Error message (if the id is not found).
    '''
    return get_id_by_name(emotion)

def get_emotion(emotion_id: int) -> str:
    '''
    Retrieve an emotion name based on a recieved emotion id.
    
    Args:
        emotion_id (int): an emotion id
    
    Returns:
        str: A JSON formated string containing either a name or an Error message (if the name is not found).
    '''
    return get_emotion_by_id_json(emotion_id)

def get_emotions():
    '''
    Retrieve the list of emotions in JSON format.
    
    Returns:
        str: A JSON string representing the list of emotions.
    '''
    return emotions_json

def get_regular_emotion(emotion_id: int) -> str:
    '''
    Retrieve an emotion based on its ID from the list of emotions. 

    Args:
        emotion_id (int): an emotion ID.
    
    Returns:
        str: the name of the emotion or an error message (if the emotion was not found).
    '''
    return get_emotion_by_id(emotion_id)