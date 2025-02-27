class Emotion:
    def __init__(self, emotion, id) -> None:
        self.emotion = emotion
        self.id = id

# Skapa en lista av Emotion-objekt baserat på feelings
feelings = {
    "happy": ["euphoric", "loving", "happy", "Euphoric", "Loving", "Happy"],
    "angry": ["furious", "frustrated", "Furious", "Frustrated"],
    "sad": ["horrified", "disappointed", "useless", "regretful", "dejected", "unhappy", "scared", "anxious", 
             "Horrified", "Disappointed", "Useless", "Regretful", "Dejected", "Unhappy", "Scared", "Anxious"]
}

# Omvandla ordboken till en lista av Emotion-objekt
emotion_objects = []
for id, (category, emotions) in enumerate(feelings.items()):
    for emotion in emotions:
        emotion_objects.append(Emotion(emotion, id))