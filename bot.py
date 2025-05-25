import re
from botbuilder.core import ActivityHandler, TurnContext, MemoryStorage, ConversationState
from db import save_user_to_db

# Initialize in-memory storage to keep track of conversation state temporarily
conversation_state = ConversationState(MemoryStorage())


class MyBot(ActivityHandler):
    def __init__(self):
        # Property to store user data like name, email, etc.
        self.user_profile_accessor = conversation_state.create_property("user_profile")
        # Property to track which step the user is currently on (e.g., 0 = first name, 1 = last name)
        self.step_accessor = conversation_state.create_property("conversation_step")

    async def on_message_activity(self, turn_context: TurnContext):
        # Get the user's message and remove leading/trailing spaces
        text = turn_context.activity.text.strip()

        # Get user data; if none exists yet, initialize as empty dictionary
        user_profile = await self.user_profile_accessor.get(turn_context, lambda: {})
        # Get current step; if it's the first time, default to step 0
        step = await self.step_accessor.get(turn_context, lambda: 0)

        # Step 0: Ask for last name after receiving first name
        if step == 0:
            user_profile["firstName"] = text
            await turn_context.send_activity("What’s your last name?")
            await self.user_profile_accessor.set(turn_context, user_profile)
            await self.step_accessor.set(turn_context, 1)

        # Step 1: Ask for date of birth
        elif step == 1:
            user_profile["lastName"] = text
            await turn_context.send_activity("What’s your date of birth? (YYYY-MM-DD)")
            await self.user_profile_accessor.set(turn_context, user_profile)
            await self.step_accessor.set(turn_context, 2)

        # Step 2: Validate and store birth date, then ask for email
        elif step == 2:
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", text):
                await turn_context.send_activity(
                    "Invalid date format. Please use YYYY-MM-DD. For example: 1995-06-23")
                return
            user_profile["birthDate"] = text
            await turn_context.send_activity("What’s your email?")
            await self.user_profile_accessor.set(turn_context, user_profile)
            await self.step_accessor.set(turn_context, 3)

        # Step 3: Ask for phone number
        elif step == 3:
            user_profile["email"] = text
            await turn_context.send_activity("What’s your phone number?")
            await self.user_profile_accessor.set(turn_context, user_profile)
            await self.step_accessor.set(turn_context, 4)

        # Step 4: Ask for street address
        elif step == 4:
            user_profile["phoneNumber"] = text
            await turn_context.send_activity("What’s your street and house number?")
            await self.user_profile_accessor.set(turn_context, user_profile)
            await self.step_accessor.set(turn_context, 5)

        # Step 5: Ask for postal code
        elif step == 5:
            user_profile["street"] = text
            await turn_context.send_activity("What’s your postal code?")
            await self.user_profile_accessor.set(turn_context, user_profile)
            await self.step_accessor.set(turn_context, 6)

        # Step 6: Ask for city
        elif step == 6:
            user_profile["postalCode"] = text
            await turn_context.send_activity("What’s your city?")
            await self.user_profile_accessor.set(turn_context, user_profile)
            await self.step_accessor.set(turn_context, 7)

        # Step 7: Ask for country
        elif step == 7:
            user_profile["city"] = text
            await turn_context.send_activity("What’s your country?")
            await self.user_profile_accessor.set(turn_context, user_profile)
            await self.step_accessor.set(turn_context, 8)

        # Step 8: Registration is complete, save all collected user data to the database
        elif step == 8:
            user_profile["country"] = text
            await self.user_profile_accessor.set(turn_context, user_profile)

            # Save final user profile to the database
            save_user_to_db(user_profile)

            # Notify user of successful registration
            await turn_context.send_activity("Registration complete! Your data has been saved.")

            # Clear user state after successful registration
            await self.user_profile_accessor.delete(turn_context)
            await self.step_accessor.delete(turn_context)

        # Save any changes to conversation state
        await conversation_state.save_changes(turn_context)

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        # Send welcome message only to users (not the bot itself)
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Hello! Would you like to register a new account? Please type your first name to begin.")
