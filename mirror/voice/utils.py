import json
import requests
import uuid
import argparse

import pyaudio
import webrtcvad
import numpy as np
import wave
import whisper

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
    
def transcribe_round(audio_file_path):
    vad_audio_capture(audio_file_path)
    transcribed_text = whisper_transcribe(audio_file_path)
    return transcribed_text

def whisper_transcribe(audio_file_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file_path)
    return result["text"]

def vad_audio_capture(output_file_path):
    FRAME_MS = 10  # Frame duration in ms
    RATE = 16000
    CHUNK_SIZE = int(RATE * FRAME_MS / 1000)
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    SILENCE_FRAMES_REQUIRED = 4000 // FRAME_MS

    vad = webrtcvad.Vad()
    vad.set_mode(3)

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE)

    print("Listening...")

    audio_buffer = []
    silence_counter = 0

    while True:
        data = stream.read(CHUNK_SIZE)
        is_speech = vad.is_speech(data, RATE)

        if is_speech:
            audio_buffer.append(data)
            silence_counter = 0
        else:
            if len(audio_buffer) > 0:
                silence_counter += 1

            if silence_counter >= SILENCE_FRAMES_REQUIRED:
                break

    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Finished recording.")
    # At this point, audio_buffer contains the audio data while you were talking
    # Save the recorded audio to a WAV file
    print(f"Saving audio to {output_file_path}")
    with wave.open(output_file_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(audio_buffer))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--utility", type=str, default="text_to_speech", help="Utility function to run")
    parser.add_argument("-t", "--text", type=str, default="Hello world", help="Text to convert to speech")
    parser.add_argument("-k", "--api-key", type=str, help="API key for ElevenLabs API")
    parser.add_argument("-v", "--voice-id", type=str, help="Voice ID for ElevenLabs API")
    parser.add_argument("-i", "--input-file", type=str, help="Input file path for whisper to transcribe")
    parser.add_argument("-o", "--output-file", type=str, default="output.wav", help="Output file path for audio")

    args = parser.parse_args()

    utility_map = {
        "text_to_speech": text_to_speech,
        "transcribe_round": transcribe_round,
        "vad_audio_capture": vad_audio_capture,
        "whisper_transcribe": whisper_transcribe
    }

    if args.utility not in utility_map:
        raise ValueError(f"Invalid utility: {args.utility}")
    
    if args.utility == "text_to_speech":
        # Check that voice_id and api_key are provided
        if not args.voice_id or not args.api_key:
            raise ValueError(f"voice_id and api_key must be provided for utility: {args.utility}")
        output_file = utility_map[args.utility](args.api_key, args.voice_id, args.text)
        print(f"Saved audio to {output_file}")
    elif args.utility == "transcribe_round":
        text = utility_map[args.utility](args.output_file)
        print(f"Transcribed text: {text}")
    elif args.utility == "vad_audio_capture":
        vad_audio_capture(args.output_file)
    elif args.utility == "whisper_transcribe":
        text = whisper_transcribe(args.output_file)
        print(f"Transcribed text:\n{text}\nfrom file: {args.output_file}")
    else:
        raise ValueError(f"Invalid utility: {args.utility}")
    