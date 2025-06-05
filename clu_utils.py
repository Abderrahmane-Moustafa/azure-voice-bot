import aiohttp
from config import settings

async def analyze_text_with_clu(text: str):
    url = f"{settings.clu_endpoint}language/:analyze-conversations?api-version=2022-10-01-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": settings.clu_api_key,
        "Content-Type": "application/json"
    }
    body = {
        "kind": "Conversation",
        "analysisInput": {
            "conversationItem": {
                "id": "1",
                "participantId": "user1",
                "text": text
            },
            "modality": "text",
            "language": "en"
        },
        "parameters": {
            "projectName": "VoiceBotRegistration",
            "deploymentName": "deployment-bot",
            "stringIndexType": "TextElement_V8"
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=body) as response:
            if response.status != 200:
                print(f"❌ Error calling CLU API: {response.status}")
                print(await response.text())
                return {"result": {"prediction": {"topIntent": "None"}}}
            result = await response.json()
            print(f"[CLU DEBUG] → Intent: {result.get('result', {}).get('prediction', {}).get('topIntent')} | Text: {text}")
            return result