# Runs the mirror agent

import os
import argparse
from playsound import playsound

from mirror.mirror_agent.agent import load_mirror_agent
from mirror.voice.utils import text_to_speech, transcribe_round

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--mirror-name", type=str, help="Name of the mirror agent")
    parser.add_argument("-a", "--mirror-architecture", type=str, default="default", help="Name of the mirror agent")
    parser.add_argument("-t", "--tools", type=str, nargs="+", required=True, choices=["chroma", "gather", "help"], help="List of tools to use")
    parser.add_argument("-d", "--data-path", type=str, default="../data/local", help="Path to your local data")
    parser.add_argument("-k", "--voice-api-key", type=str, default=None, help="ElevenLabs API Key")
    parser.add_argument("-v", "--voice-out", type=bool, default=False, help="Boolean flag to use text-to-speech on Mirror output")
    parser.add_argument("-vi", "--voice-id", type=str, default=os.environ.get("ELEVENLABS_VOICE_ID"), help="Voice ID to use for text-to-speech on Mirror output")
    parser.add_argument("-ti", "--transcribe-input", type=bool, default=False, help="Boolean flag to transcribe user input instead of using text input")
    parser.add_argument("-g", "--greeting", type=str, required=True, help="First sentence to say to the Mirror")
    parser.add_argument("-tr", "--training-mode", type=bool, default=False,
                        help="[Coming Soon] Boolean flag to make True if data from this session should be used to further train the mirror")

    args = parser.parse_args()

    mirror = load_mirror_agent(
        mirror_name=args.mirror_name,
        architecture=args.mirror_architecture,
        tools=args.tools,
        data_path=args.data_path,
        voice_out=args.voice_out,
        voice_id=args.voice_id,
    )

    next_input = args.greeting
    while True:
        print(f"Continuing conversation with: {next_input}")
        print(type(next_input))
        mirror_response = mirror.run(next_input)
        if args.voice_out:
            audio_file = text_to_speech(api_key=args.voice_api_key, voice_id=args.voice_id, text=mirror_response)
            playsound(audio_file)
        if args.transcribe_input:
            print("Transcribing input...")
            next_input = transcribe_round("/tmp/mirror.wav")
        else:
            next_input = input("Enter your next input: ")
