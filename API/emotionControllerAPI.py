import emotionAPI

def negated_feeling(feeling: str) -> str:
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



            