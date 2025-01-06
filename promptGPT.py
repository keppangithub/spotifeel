from openai import OpenAI
#installera openai med: pip install openai
#Exportera nyckeln i VS terminal med kommandot nedan
#Byt ut "api_key" mot den faktiska nyckeln
#export OPENAI_API_KEY="api_key"

client = OpenAI(api_key = "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")


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
    print(songs)

    return songs
