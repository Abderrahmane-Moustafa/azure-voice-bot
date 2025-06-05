import re
from botbuilder.core import ActivityHandler, TurnContext, MemoryStorage, ConversationState
from clu_utils import analyze_text_with_clu
from db import save_user_to_db

conversation_state = ConversationState(MemoryStorage())

class MyBot(ActivityHandler):
    def __init__(self):
        self.user_profile_accessor = conversation_state.create_property("user_profile")

    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text.strip()
        user_profile = await self.user_profile_accessor.get(turn_context, lambda: {})

        clu_response = await analyze_text_with_clu(text)
        prediction = clu_response.get("result", {}).get("prediction", {})
        intent = prediction.get("topIntent", "None")
        entities = prediction.get("entities", [])

        def extract(entity_name):
            for e in entities:
                if e.get("category") == entity_name:
                    return e.get("text")
            return None

        reply = None

        if intent == "ProvideConfirmInput":
            reply = "✅ Great! What’s your first name?"

        elif intent == "ProvideRejectInput":
            reply = "👍 No problem. If you change your mind, just let me know!"

        elif intent == "ProvideFirstName":
            user_profile["firstName"] = extract("firstName") or text
            reply = "What’s your last name?"

        elif intent == "ProvideLastName":
            user_profile["lastName"] = extract("lastName") or text
            reply = "What’s your date of birth? (YYYY-MM-DD)"

        elif intent == "ProvideDateOfBirth":
            dob = extract("birthDate")
            if dob and re.match(r"^\d{4}-\d{2}-\d{2}$", dob):
                user_profile["birthDate"] = dob
                reply = "What’s your email?"
            else:
                reply = "❌ Invalid date format. Please use YYYY-MM-DD."

        elif intent == "ProvideEmail":
            user_profile["email"] = extract("email") or text
            reply = "What’s your phone number?"

        elif intent == "ProvidePhoneNumber":
            user_profile["phoneNumber"] = extract("phoneNumber") or text
            reply = "What’s your street name?"

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
            save_user_to_db(user_profile)  # ← make sure this matches your DB schema
            reply = "✅ Registration complete! Your data has been saved."
            await self.user_profile_accessor.delete(turn_context)

        else:
            reply = "❓ I didn’t understand that. Could you try rephrasing?"

        await turn_context.send_activity(reply)
        await self.user_profile_accessor.set(turn_context, user_profile)
        await conversation_state.save_changes(turn_context)

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "👋 Hello! Say something like ‘I want to register’ to begin."
                )
