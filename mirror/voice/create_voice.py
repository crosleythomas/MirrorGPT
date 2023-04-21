import os
import argparse
import sounddevice as sd
import requests
import wavio

VOICE_CLONE_STRING = """
    Welcome to the world of voice cloning. Voice cloning is an emerging technology that has the potential
    to revolutionize the way we interact with computers and other digital devices.
    By creating a digital model of a person's voice, voice cloning tools can generate synthetic speech that
    sounds like the real thing.

    The process of voice cloning involves analyzing a person's voice and identifying its unique characteristics,
    such as pitch, tone, and cadence. This information is then used to create a digital voice model,
    which can be used to generate new speech that sounds like the original speaker.

    Voice cloning technology has many potential applications. In the entertainment industry,
    it could be used to create digital versions of actors and other performers.
    Virtual assistants,such as Siri and Alexa, could be personalized to sound like specific individuals,
    making them more engaging and relatable. And for people with speech impairments,
    voice cloning could provide a powerful new tool for communication.

    However, voice cloning also raises important ethical questions.
    If someone's voice can be cloned without their consent, it could be used to create fake audio recordings
    or to impersonate them in other ways. As with any new technology, it's important to approach voice cloning
    with caution and to consider its potential impact on privacy and security.

    In conclusion, voice cloning is a fascinating new technology with many potential applications.
    As the field continues to develop, it will be interesting to see how it evolves and how it impacts our lives.

    Popcorn is a beloved snack food that has been enjoyed for centuries.
    But where did this delicious treat come from?
    The origins of popcorn can be traced back to ancient times, when the Aztecs and
    other indigenous peoples in Mexico would roast ears of corn over an open flame until the kernels popped.

    When the Spanish conquistadors arrived in Mexico in the 16th century, they were introduced to this unique snack food.
    The Spanish were fascinated by the sound of the popping corn and brought it back to Europe with them.
    Popcorn soon became a popular snack in Spain and other European countries.

    In the 19th century, popcorn became a popular snack food in the United States, particularly at circuses, fairs,
    and other public events.
    The first commercial popcorn machine was invented by Charles Cretors in 1885,
    and it quickly became a fixture at movie theaters and other entertainment venues.
    """

def capture_voice_sample(output_file):
    sample_rate = 16000
    instructions = f"""
        You will be presented with a long passage to read aloud.
        This  will record for 1 minute and then stop.

        Prease 'Enter' to see the passage and start recording.
    """
    print(instructions)
    input()

    text = f"""
        Please read the following text aloud:
        {VOICE_CLONE_STRING}
    """
    print(text)

    recording = record_audio(sample_rate)
    save_audio_to_file(recording, output_file, sample_rate)

def record_audio(sample_rate):
    print("Recording...")
    duration = 10
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    return recording

def save_audio_to_file(recording, filename, sample_rate):
    wavio.write(filename, recording, sample_rate, sampwidth=2)
    print(f"Audio saved to {filename}")

def create_voice(filename, user_id, api_key):
    url = "https://api.elevenlabs.io/v1/voices/add"
    print(f"Creating new voice for user {user_id} at endpoint {url}")

    payload = {"name": f"{user_id} Mirror voice"}
    files = [('files',(filename, open(filename,'rb'),'audio/wav'))]
    headers = {'xi-api-key': api_key}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    if response.status_code == 200:
        print("Voice created successfully")
    else:
        print(f"Voice creation failed with code {response.status_code}")
    print(response.text)

def main(user_id, input_file, output_file, api_key):
    if not input_file:
        capture_voice_sample(output_file)
        input_file = output_file
    create_voice(input_file, user_id, api_key)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user-id", type=str, help="User ID for ElevenLabs to upload the audio to")
    parser.add_argument("-i", "--input-file", default=None, type=str, help="Path to the input file containing a voice recording")
    parser.add_argument("-o", "--output-file", default="/tmp/voice_data.wav", type=str, help="Path to the output file for creating a new voice recording")
    parser.add_argument("-k", "--api-key", type=str, help="ElevenLabs API key")
    args = parser.parse_args()

    if args.api_key is None:
        if "ELEVEN_LABS_API_KEY" not in os.environ:
            print("Please provide an Eleven Labs API key")
            exit(1)
        args.api_key = os.environ.get("ELEVEN_LABS_API_KEY")
    main(args.user_id, args.input_file, args.output_file, args.api_key)
