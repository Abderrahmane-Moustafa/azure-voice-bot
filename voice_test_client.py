import os
import json
import uuid
import requests
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Load environment variables from .env
load_dotenv()

# Speech config
speech_key = os.getenv("speech_key")
speech_region = os.getenv("speech_region")

def recognize_speech():
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("🎤 Speak now...")
    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"🗣️ You said: {result.text}")
        return result.text
    else:
        print("❌ Could not recognize speech.")
        return None

def send_to_bot(text):
    url = "http://localhost:3978/api/messages"
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "type": "message",
        "from": {"id": "user1", "name": "User"},
        "text": text,
        "recipient": {"id": "bot", "name": "Bot"},
        "conversation": {"id": str(uuid.uuid4())},
        "id": str(uuid.uuid4()),
        "channelId": "console",
        "serviceUrl": "http://localhost"
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))
    if response.status_code in (200, 201):
        print("✅ Message sent to bot.")
        if response.content:
            print("🤖 Bot response:", response.json())
    else:
        print("❌ Failed to send message to bot:", response.status_code)
        print(response.text)

if __name__ == "__main__":
    text = recognize_speech()
    if text:
        send_to_bot(text)
