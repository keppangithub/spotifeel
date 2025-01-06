from openai import OpenAI
#installera openai med: pip install openai
#Exportera nyckeln i VS terminal med kommandot nedan
#Byt ut "api_key" mot den faktiska nyckeln
#export OPENAI_API_KEY="api_key"

client = OpenAI()

def run_prompt(text):
    completion = client.chat.completions.create(
     model="gpt-3.5-turbo",
         messages=[
        {"role": "system", "content": "Your task is to determine which of the following feelings suits the text the most: furious, frustrated, horrified, disappointed, euphoric, loving, happy, useless, regretful, dejected, unhappy, scared, and anxious. Respond with only one of these words."},
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
        {"role": "system", "content": "Your task is to give 6 recomendations for songs that can be found on spotify based on the emotion you recieve. The recommendations shall be written as JSON Objects and follow this structure: song title, artist"},
        {
            "role": "user",
            "content":'"'+emotion+'"'
        }
] 
)
    print(completion)
    songs = completion.choices[0].message
    #songs = str(response_content).split("content='")[1].split("'")[0]
    print(songs)

    return songs


