import json

class Emotion:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
    
    def to_dict(self):
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

def get_id_by_name(name: str) -> str:
    '''
    Retrieves the ID of an emotion based on its name.
    Returns JSON with id or an error message if not found.
    '''
    for e in emotions:
        if e.name.lower() == name.lower():
            return json.dumps({"id": e.id})
    return json.dumps({"error": "Emotion not found"})

def get_emotion_by_id(emotion_id: int) -> str:
    '''
    Retrieves an emotion based on its ID.
    Returns JSON with emotion name or an error message if not found.
    '''
    for e in emotions:
        if e.id == emotion_id:
            return json.dumps(e.to_dict())
    return json.dumps({"error": "Emotion not found"})

emotions_json = json.dumps([e.to_dict() for e in emotions], indent=10)