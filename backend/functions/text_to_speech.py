import requests
from decouple import config

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")


def convert_text_to_speech(message):
    body = {
        "text": message,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0,
            "style": 0.5,
            "use_speaker_boost": True
        }
    }

    voice_bella = "EXAVITQu4vr4xnSDxMaL"

    headers = {
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_bella}"

    try:
        response = requests.post(endpoint, json=body, headers=headers)

    except Exception as e:
        print(e)
        return None
  
    if response.status_code != 200:
        print(response.status_code)
        return None
    
    return response.content