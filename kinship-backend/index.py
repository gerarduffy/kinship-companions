import os
from uuid import uuid4

from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/api/voices", methods=["GET"])
def get_voices():
    url = "https://api.elevenlabs.io/v1/voices"
    api_key = os.environ.get('XI_API_KEY')

    headers = {
      "Accept": "application/json",
      "xi-api-key": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.content, 200
    else:
        return {"error": "Cannot fetch voices"}, response.status_code


@app.route("/api/healthchecker", methods=["GET"])
def healthchecker():
    return {"status": "success", "message": "Integrate Flask Framework with Next.js"}


XI_API_KEY = os.environ.get('XI_API_KEY')
VOICE_SAMPLE_PATH1 = "<path-to-file>"
VOICE_SAMPLE_PATH2 = "<path-to-file>"
OUTPUT_PATH = "voice_tests/voice_test.mp3"
VOICE_ID = os.environ.get('VOICE_ID')


@app.route("/api/history", methods=["GET"])
def get_history():
    history_url = "https://api.elevenlabs.io/v1/history"
    headers = {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY
    }

    response = requests.get(history_url, headers=headers)
    return response.text


@app.route("/api/text-to-speech/<voice_id>", methods=["POST"])
def text_to_speech(voice_id):
    CHUNK_SIZE = 1024
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": request.json.get("text"),
        "model_id": "eleven_monolingual_v1",
        "voice_settings": request.json.get("voice_settings")
    }

    response = requests.post(tts_url, json=data, headers=headers)

    curr_audio_output_path = f"voice_tests/{uuid4().hex}.mp3"

    with open(curr_audio_output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    return {"status": "success"}, 200


@app.route("/api/add-voice", methods=["POST"])
def add_voice():
    add_voice_url = "https://api.elevenlabs.io/v1/voices/add"

    headers = {
        "Accept": "application/json",
        "xi-api-key": XI_API_KEY
    }

    data = {
        'name': 'Voice name',
        'labels': '{"accent": "American", "gender": "Female"}',
        'description': 'An old American male voice with a slight hoarseness in his throat. Perfect for news.'
    }

    files = [
        ('files', ('sample1.mp3', open(VOICE_SAMPLE_PATH1, 'rb'), 'audio/mpeg')),
        ('files', ('sample2.mp3', open(VOICE_SAMPLE_PATH2, 'rb'), 'audio/mpeg'))
    ]

    response = requests.post(add_voice_url, headers=headers, data=data, files=files)

    return response.json(), response.status_code


@app.route("/api/settings/default", methods=["GET"])
def get_default_settings():
    response = requests.get(
        "https://api.elevenlabs.io/v1/voices/settings/default",
        headers={"Accept": "application/json"}
    ).json()

    return response, 200


if __name__ == "__main__":
    # export all the environment variables

    app.run()
