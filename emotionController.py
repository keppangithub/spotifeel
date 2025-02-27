class EmotionController:
    def __init__(self) -> None:
        self.emotions = {
            "happy": ["euphoric", "loving", "happy", "Euphoric", "Loving", "Happy"],
            "angry": ["furious", "frustrated", "Furious", "Frustrated"],
            "sad": ["horrified", "disappointed", "useless", "regretful", "dejected", "unhappy", "scared", "anxious", "Horrified", "Disappointed", "Useless", "Regretful", "Dejected", "Unhappy", "Scared", "Anxious", "sad", "Sad"]
        } 

    def get_emotions(self, emotion: str) -> list:  
        '''
        Check what category the emotion received from OPEN AI API is part of in order to return a relevant message to the user
        
        parameter:
        - a emotion (str)
        
        returns:
        - a message (str)
        '''
        
        for category, emotion_list in self.emotions.items():
            if emotion in emotion_list:
                
                if category == "happy":
                    return ["Det verkar som du haft en bra dag idag!", "Fortsätt i samma vibe", "Lugna ner"]
                
                if category == "angry":
                    return ["Det verkar som idag har varit en frustrerande dag.", "Få ut ilskan", "Muntra upp"]
                
                if category == "sad":
                    return ["Det verkar som om du haft en jobbig dag.", "Grotta i känslan ett tag", "Muntra upp"]

        return "Emotion not found."
