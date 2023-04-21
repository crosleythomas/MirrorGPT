import json
import requests
import uuid

def text_to_speech(api_key, voice_id, text):
    print(f"Running text_to_speech with api_key: {api_key}, voice_id: {voice_id}, text: {text}")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    payload = json.dumps({
        "text": text,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
    })
    headers = {
        'xi-api-key': api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        output_file = f"/tmp/{uuid.uuid4()}.wav"
        with open(output_file, "wb") as f:
            f.write(response.content)
        return output_file
    else:
        raise ValueError(f"Error in text_to_speech: {response.content}, {response.status_code}")