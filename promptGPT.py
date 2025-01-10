from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=key)
prompt_counter = 0

def is_emotion_valid(emotion: str) -> bool:
    '''
    Check if the emotion received from the 'run_prompt' function is one of the valid feelings.
    
    Valid feelings: 
    - Furious
    - Frustrated
    - Horrified
    - Disappointed
    - Euphoric
    - Loving
    - Happy
    - Useless
    - Regretful
    - Dejected
    - Unhappy
    - Scared
    - Anxious
    
    Returns Boolean (depending on if the feeling received is valid or not)
    '''
    valid_feelings = ['furious', 'frustrated', 'horrified', 'disappointed', 'euphoric', 'loving', 'happy', 'useless', 'regretful', 'dejected', 'unhappy', 'scared','anxious']
    
    if emotion.lower() in valid_feelings:
        print(emotion)
        print('True')
        return True
    
    else: 
        print(emotion)
        print('False')
        return False


def run_prompt(text: str) -> str:
    '''
    Take the user input, diary entry, as an argument. Use OPEN AI API to get back the emotion which corresponds best with the user input.
    
    Check if the emotion is valid via the is_emotion_valid function.
    
    Returns: 
    - emotion (str)
    '''
    completion = client.chat.completions.create(
     model="gpt-3.5-turbo",
         messages=[
        {"role": "system", "content": "Your task is to determine which of the following feelings, and only one of the following feeling suits the text the most: furious, frustrated, horrified, disappointed, euphoric, loving, happy, useless, regretful, dejected, unhappy, scared, and anxious. Respond with only one of these words in english and without capital letters."},
        {
            "role": "user",
            "content":'"'+text+'"'
        }
]
)
    response_content = completion.choices[0].message
    emotion = str(response_content).split("content='")[1].split("'")[0]
    
    if is_emotion_valid(emotion):
        return emotion
    
    else:
        if(prompt_counter<10):
            run_prompt(text)
            prompt_counter+1

def create_playlist(emotion):
    completion = client.chat.completions.create(
     model="gpt-3.5-turbo",
         messages=[
        {"role": "system", "content": "Your task is to give 6 recomendations for songs that can be found on spotify based on the emotion you recieve. The recommendations shall follow this structure: song title, artist and ONLY contain this."},
           {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": '"'+emotion+'"'
        }
      ]
    }
]
)
    songs = completion.choices[0].message.content
    print(songs)
    
    formated_songs = []
    
    for song in songs.split("\n"):
        if ". " in song:
            title_artist = song.split(". ", 1)[1]
            title_artist = title_artist.replace('"', '')
            title_artist = title_artist.replace(' by ', ',')
            
            formated_songs.append([title_artist])
                
    print(formated_songs)            
    
    return formated_songs
