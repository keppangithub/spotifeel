def get_feelings(feeling):  
    feelings = {
        "happy": ["euphoric", "loving", "happy", "Euphoric", "Loving", "Happy"],
        "angry": ["furious", "frustrated", "Furious", "Frustrated"],
        "sad": ["horrified", "disappointed", "useless", "regretful", "dejected", "unhappy", "scared", "anxious", "Horrified", "Disappointed", "Useless", "Regretful", "Dejected", "Unhappy", "Scared", "Anxious", "sad", "Sad"]
    } 
    for category, feelings in feelings.items():
        if feeling in feelings:
            if category == "happy":
                return ["Det verkar som du haft en bra dag idag!", "Fortsätt i samma vibe.", "Lugna ner"]
            if category == "angry":
                return ["Det verkar som idag har varit en frustrerande dag.", "Få ut ilskan", "Muntra upp"]
            if category == "sad":
                return ["Det verkar som om du haft en jobbig dag.", "Grotta i känslan ett tag", "Muntra upp"]

    return "Feeling not found"


def negated_feeling(feeling):
    feelings = {
        "happy": ["euphoric", "loving", "happy", "Euphoric", "Loving", "Happy"],
        "angry": ["urious", "frustrated", "Furious", "Frustrated"],
        "sad": ["horrified", "disappointed", "useless", "regretful", "dejected", "unhappy", "scared", "anxious", "Horrified", "Disappointed", "Useless", "Regretful", "Dejected", "Unhappy", "Dcared", "Anxious"]
    } 
    for category, feelings in feelings.items():
        if feeling in feelings:
            if category == "happy":
                print("Negated category = sad")
                return "sad"
            if category == "angry":
                print("Negated category = chill")
                return "chill"
            if category == "sad":
                print("Negated category = happy")
                return "happy"
            
