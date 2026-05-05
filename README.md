# Spotifeel

Spotifeel is a mashup service combining the Spotify and OpenAI APIs to generate personalized playlists based on your mood.

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: JavaScript
- **APIs**: Spotify Web API, OpenAI API
- **Docs**: Swagger UI

## Setup

**1. Install dependencies**

```bash
python -m pip install --upgrade pip
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Create a `.env` file** in the project root:

```env
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
OPENAI_API_KEY=your_openai_api_key
```

**3. Run the app**

Start the API server in one terminal:

```bash
cd API && python main.py
```

Start the client in another:

```bash
cd client && python main.py
```

Then open [http://127.0.0.1:8888](http://127.0.0.1:8888).

## API Docs

Run the API server, log in, then visit [http://127.0.0.1:8888/docs](http://127.0.0.1:8888/docs).

## Tests

```bash
pytest                          # run all tests
pytest -v                       # verbose output
pytest --cov --cov-report=term  # with coverage
```
