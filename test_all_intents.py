import asyncio
from clu_utils import analyze_text_with_clu

# جمَل تمثل كل intent محتمل
test_inputs = {
    "ProvideFirstName": "My name is John",
    "ProvideLastName": "My last name is Doe",
    "ProvideDateOfBirth": "I was born on 1990-01-01",
    "ProvideEmail": "My email is test@example.com",
    "ProvidePhoneNumber": "My phone number is 1234567890",
    "ProvideAddress": "My address is Main Street 10B",
    "ProvidePostalCode": "My postal code is 14050",
    "ProvideCity": "I live in Berlin",
    "ProvideCountry": "My country is Germany",
    "ProvideConfirmInput": "Yes please continue",
    "ProvideRejectInput": "No thanks",
}

async def test_all():
    for intent, text in test_inputs.items():
        print(f"\nTesting intent: {intent}")
        result = await analyze_text_with_clu(text)
        top_intent = result['result']['prediction']['topIntent']
        confidence = result['result']['prediction']['intents'][0]['confidenceScore']
        print(f"Input: {text}")
        print(f"Predicted intent: {top_intent} (Confidence: {confidence:.2f})")

if __name__ == "__main__":
    asyncio.run(test_all())
