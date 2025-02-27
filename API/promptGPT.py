from dotenv import load_dotenv
from openai import OpenAI
import os
import emotionControllerAPI

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

    returns:
    - Boolean (depending on if the feeling received is valid or not)
    '''
    valid_feelings = ['furious', 'frustrated', 'horrified', 'disappointed', 'euphoric', 'loving', 'happy', 'useless', 'regretful', 'dejected', 'unhappy', 'scared','anxious']

    if emotion.lower() in valid_feelings:
        return True

    else:
        return False


def run_prompt(text: str) -> str:
    '''
    Take the user input, diary entry, as an argument. Use OPEN AI API to get back the emotion which corresponds best with the user input.

    Check if the emotion is valid via the is_emotion_valid function.

    returns:
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

def create_playlist(input) -> list:
    emotion = None

    if isinstance(input,int):
        print(input)
        emotion = emotionControllerAPI.get_regular_emotion(input)
    else:
        emotion=input
    
    '''
    Get six recommended songs based on a received emotion (argument).
    Manipulate them to a specific format and add to the list formated_songs

    parameter:
    - emotions (str)

    returns:
    - formated_songs (list)
    '''
    completion = client.chat.completions.create(
     model="gpt-3.5-turbo",
         messages=[
        {"role": "system", "content": "Your task is to give 6 recomendations for songs that can be found on spotify based on the emotion you recieve. The recommendations shall follow this structure: song title, artist and ONLY contain this."},
           {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": '"'+str(emotion)+'"'
        }
      ]
    }
]
)
    songs = completion.choices[0].message.content

    formated_songs = []

    for song in songs.split("\n"):
        if ". " in song:
            title_artist = song.split(". ", 1)[1]
            title_artist = title_artist.replace('"', '')
            title_artist = title_artist.replace(' by ', ',')

            formated_songs.append([title_artist])

    return formated_songs
