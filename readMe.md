# Spotifeel

Spotifeel is a mashup service that combines APIs from Spotify and OpenAI to create personalized playlists based on the user's mood.

## Programming Languages

- Python
- JavaScript

### Required python modules

- requests (2.32.3)
- dotenv (1.0.1)
- openai (1.60.2)
- flask-swagger-ui (4.11.1)
- pyyaml (6.0.2)
- Flask (3.1.0)

### Installation process

**Make sure pip3 is latest version.**
```
python3 -m pip install --upgrade pip
python3 -m venv venv
pip3 install -r requirements.txt
```

Firstly upgrade pip - python.exe\
-m pip install --upgrade pip\
\
Then install all modules by typing
- pip install -r requirements.txt

**In order to run the mashup service you need to create a .env file in which you should put the received keys like this**\
CLIENT_ID='PUT KEY HERE'\
CLIENT_SECRET='PUT KEY HERE'\
OPENAI_API_KEY='PUT KEY HERE'

Next step is to run the file main.py. Then go to <http://127.0.0.1:8888> where the website will be running.

To view the API documentation run main.py and go to this URL <http://127.0.0.1:8888>, make sure you are logged in and then go to this URL  <http://127.0.0.1:8888/docs>.
