import re
from speech_utils import recognize_speech
from botbuilder.core import ActivityHandler, TurnContext, MemoryStorage, ConversationState
from clu_utils import analyze_text_with_clu
from db import save_user_to_db

conversation_state = ConversationState(MemoryStorage())

class MyBot(ActivityHandler):
    def __init__(self):
        self.user_profile_accessor = conversation_state.create_property("user_profile")

    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text.strip()

        # Handle empty input
        if not text:
            await turn_context.send_activity("⚠️ I didn’t catch that. Could you repeat it, please?")
            return

        print(f"[USER]: {text}")
        user_profile = await self.user_profile_accessor.get(turn_context, lambda: {})

        # Analyze with CLU
        clu_response = await analyze_text_with_clu(text)
        prediction = clu_response.get("result", {}).get("prediction", {})
        intent = prediction.get("topIntent", "None")
        entities = prediction.get("entities", [])

        print(f"[CLU] Intent: {intent} | Entities: {entities}")
        reply = None

        def extract(entity_name):
            for e in entities:
                if e.get("category") == entity_name:
                    return e.get("text")
            return None

        # Fallback
        if intent == "None" or intent == "NoneIntent":
            reply = "🤖 Sorry, I didn't understand that. Can you rephrase?"

        elif intent == "ProvideConfirmInput":
            reply = "Great! What’s your first name?"

        elif intent == "ProvideRejectInput":
            reply = "No problem. If you change your mind, just let me know!"

        elif intent == "ProvideFirstName":
            user_profile["firstName"] = extract("firstName") or text
            reply = "What’s your last name?"

        elif intent == "ProvideLastName":
            user_profile["lastName"] = extract("lastName") or text
            reply = "What’s your date of birth? (YYYY-MM-DD)"

        elif intent == "ProvideDateOfBirth":
            dob = extract("birthDate") or text
            if re.match(r"^\d{4}-\d{2}-\d{2}$", dob):
                user_profile["birthDate"] = dob
                reply = "What’s your email?"
            else:
                reply = "❌ Invalid date format. Please use YYYY-MM-DD."

        elif intent == "ProvideEmail":
            email = extract("email") or text
            if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
                user_profile["email"] = email
                reply = "What’s your phone number?"
            else:
                reply = "❌ That doesn’t look like a valid email. Please enter a correct email address."

        elif intent == "ProvidePhoneNumber":
            phone = extract("phoneNumber") or text
            if re.match(r"^\+?\d{6,15}$", phone):
                user_profile["phoneNumber"] = phone
                reply = "What’s your street name?"
            else:
                reply = "❌ That doesn’t look like a valid phone number. Please try again."

        elif intent == "ProvideStreet":
            user_profile["street"] = extract("street") or text
            reply = "What’s your house number?"

        elif intent == "ProvideHouseNumber":
            user_profile["houseNumber"] = extract("houseNumber") or text
            reply = "What’s your postal code?"

        elif intent == "ProvidePostalCode":
            user_profile["postalCode"] = extract("postalCode") or text
            reply = "What’s your city?"

        elif intent == "ProvideCity":
            user_profile["city"] = extract("city") or text
            reply = "What’s your country?"

        elif intent == "ProvideCountry":
            user_profile["country"] = extract("country") or text
            save_user_to_db(user_profile)
            reply = "✅ Registration complete! Your data has been saved."
            await self.user_profile_accessor.delete(turn_context)

        else:
            reply = "🤔 I'm not sure how to help with that. Can you try again?"

        # Send reply
        await turn_context.send_activity(reply)
        await self.user_profile_accessor.set(turn_context, user_profile)
        await conversation_state.save_changes(turn_context)

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "👋 Hello! Say something like ‘I want to register’ to begin."
                )
