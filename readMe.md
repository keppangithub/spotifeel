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

Note: You might have to write python3 instead of python for it to work

**Make sure you have the latest version of pip**

```
python -m pip install --upgrade pip
```

**Start a virtual environment**\
Linux/macOS

```
python -m venv venv
```

Windows

```
python -m venv myenv
```

**Activate the virtual environment**
Linux/macOS

```
. venv/bin/activate
```

Windows

```
venv\Scripts\activate
```

**Install the required Python packages**
```
pip install -r requirements.txt
```

**In order to run the mashup service you need to create a .env file in which you should put the received keys like this**\
CLIENT_ID='PUT KEY HERE'\
CLIENT_SECRET='PUT KEY HERE'\
OPENAI_API_KEY='PUT KEY HERE'

Run the file main.py located **in the map API** in a terminal.
Next, run the file main.py located **in the client map** in another terminal.

Then go to <http://127.0.0.1:8888> where the website will be running.

**API Documentation**\
To view the API documentation run main.py and go to this URL <http://127.0.0.1:8888>, make sure you are logged in and then go to this URL: <http://127.0.0.1:8888/docs>
