def get_emotions(emotion: str) -> list:  
    '''
    Check what category the emotion received from OPEN AI API is part
    of in order to return a relevant message to the user
    
    Args:
        emotion (str)
    
    Returns:
        A message (str)
    '''
    emotions = {
    "happy": ["euphoric", "loving", "happy", "Euphoric", "Loving", "Happy"],
    "angry": ["urious", "frustrated", "Furious", "Frustrated"],
    "sad": ["horrified", "disappointed", "useless", "regretful", "dejected", "unhappy", "scared", "anxious", "Horrified", "Disappointed", "Useless", "Regretful", "Dejected", "Unhappy", "Dcared", "Anxious"]
} 
    
    for category, emotion_list in emotions.items():
        if emotion in emotion_list:
            
            if category == "happy":
                return ["Det verkar som du haft en bra dag idag!", "Fortsätt i samma vibe", "Lugna ner"]
            
            if category == "angry":
                return ["Det verkar som idag har varit en frustrerande dag.", "Få ut ilskan", "Muntra upp"]
            
            if category == "sad":
                return ["Det verkar som om du haft en jobbig dag.", "Grotta i känslan ett tag", "Muntra upp"]

    return "Emotion not found."
