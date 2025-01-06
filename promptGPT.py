from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=key)


def run_prompt(text):
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
    print(emotion)
    return emotion


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
    songs = [line.split(". ", 1)[1] for line in songs.split("\n")]
    formatted_songs = [
    song.replace('"', "")  # Remove all quotes from the song titles
    for song in songs
   ]
    print(formatted_songs)

    return songs
