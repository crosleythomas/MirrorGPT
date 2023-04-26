# Voice Integration

## Text to Speech
This package contains utilities for connecting text-to-speech models for giving your Mirror Agent a voice.

There are 3 main pieces to solve:
1. Getting sample data of your voice (either by manually recording sample audio or pulling it from existing sources like your Zoom calls)
2. Create a voice clone
3. Integrating that voice with the Mirror Agent's text output

## Curent Integrations
- [ElevenLabs](https://beta.elevenlabs.io/)

## Contribution Wishlist
- [ ] Add Suno AI's [bark](https://github.com/suno-ai/bark) project

## Speech to Text

Speech-to-Text is useful in MirrorGPT in the following ways:
1. Creating speech -> speech interfaces with a Mirror Agent
2. Creating conversational datasets for Mirror LLM fine-tuning from spoken conversational data

### Speech-To-Text Model
There has been a large increase in publicly available STT models since the launch of [Whisper](https://openai.com/research/whisper) by OpenAI.

We have the following criteria when selecting the best STT model to integrate with Mirror
1. Free/OSS and ability to run locally - important for our privacy principle and integrating with the rest of the stack that runs locally
2. Accuracy
3. Streaming - to make the experience feel like a real conversation, we want this to run as close to real-time as possible
