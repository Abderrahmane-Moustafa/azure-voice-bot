import azure.cognitiveservices.speech as speechsdk
from config import settings

def recognize_speech():
    speech_config = speechsdk.SpeechConfig(subscription=settings.speech_key, region=settings.speech_region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("🎤 Speak into your microphone...")

    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "❌ No speech could be recognized."
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        return f"❌ Speech recognition canceled: {cancellation_details.reason}"
