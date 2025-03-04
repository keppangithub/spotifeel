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
    
    Args:
        emotion (str): an emotion name.

    Returns:
        boolean: depending on if the feeling received is valid or not.
    '''
    valid_feelings = ['furious', 'frustrated', 'horrified', 'disappointed', 'euphoric', 'loving', 'happy', 'useless', 'regretful', 'dejected', 'unhappy', 'scared','anxious']

    if emotion.lower() in valid_feelings:
        return True

    else:
        return False


def run_prompt(text: str) -> str:
    '''
    Use OPEN AI's API to retrieve the emotion which best corresponds with the user input.
    Check if the emotion is valid via the is_emotion_valid function.
    
    Args:
        text (str): users diary entry/prompt.

    Returns:
        emotion (str): an emotion name.
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
        else:
            return "Error, couldn't define a feeling."

def create_playlist(input: int) -> list:
    '''
    Get six recommended songs based on a received emotion.
    Manipulate them to a specific format and add to the list formated_songs

    Args:
        input (int): an emotion id.

    Returns:
        list: a list of formated playlists containing the title and the artist.
    '''
    emotion = None

    if isinstance(input,int):
        emotion = emotionControllerAPI.get_regular_emotion(input)
        
    else:
        emotion=input
    
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

    
    return format_playlist(formated_songs)

def format_playlist(song_list: list) -> dict:
    '''
    Format a list of songs into a dictionary with a key called 'tracks' containing song information.

    Args:
        song_list (list): A list of songs with information about the artist and song title.
        
    Returns:
        dict: A dictionary containing a key called 'tracks', which is a list of dictionaries. Each dictionary represents a song with 'titel' and 'artists' as keys.
    '''
    tracks = {'tracks' : []}

    for song in song_list:
        if len(song) != 1:
            continue

        track_info = song[0].split(",")
        track_name = track_info[0].strip()
        track_artist = track_info[1].strip()

        track = {
            "titel": track_name,
            "artists": track_artist
        }
        
        tracks['tracks'].append(track)
    
    return tracks
