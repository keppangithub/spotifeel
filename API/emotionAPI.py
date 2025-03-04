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