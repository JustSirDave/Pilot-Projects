import json
import random
from datetime import datetime, timedelta, timezone, time
import re
import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')

# Load intents from intents.json file
with open("intents.json", "r") as file:
    intents = json.load(file)["intents"]


# Helper function to get a response based on user input
"""
def get_response(user_input):
    user_input = user_input.lower()

    # Iterate through intents to find a matching pattern
    for intent in intents:
        for pattern in intent["patterns"]:
            if pattern in user_input:
                if intent["tag"] == "time":
                    current_time = datetime.now().strftime("%I:%M %p")  # Format as HH:MM AM/PM
                    return f"The current time is {current_time}."

                return random.choice(intent["responses"])

    # Fallback response if no pattern is matched
    return "I'm not sure how to respond to that. Try asking something else, or say 'bye' to end the chat!"
"""


def get_response(user_input, user_name, previous_intent=None):
    user_input = user_input.lower()

    # Placeholder for current time
    current_time = datetime.now().strftime("%I:%M %p")

    for intent in intents:
        for pattern in intent["patterns"]:
            # Check for exact pattern match or synonym match
            if pattern in user_input or any(is_synonym(word, pattern) for word in user_input.split()):

                # Special handling for dynamic time response
                if intent["tag"] == "time":
                    return f"The current time is {current_time}."

                # Personalize responses
                response = random.choice(intent["responses"])
                if "{user_name}" in response:
                    response = response.replace("{user_name}", user_name)
                if "{current_time}" in response:
                    response = response.replace("{current_time}", current_time)

                # Track previous intent for follow-ups
                previous_intent = intent["tag"]

                return response

    # Fallback response if no pattern is matched
    return "I'm not sure how to respond to that. Try asking something else, or say 'bye' to end the chat!"


def is_synonym(word, pattern):
    synonyms = set()
    for syn in wordnet.synsets(pattern):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return word in synonyms

# Step 1: Greeting the User
print("Hello! What's your name?")
user_name = input()  # Get the user's name
print(f"Nice to meet you, {user_name}!")

# Step 2: Basic Conversation Loop
while True:
    print("How can I help you today?")
    user_input = input().lower()  # Get user's conversational prompt

    # Check for goodbye patterns directly to exit the program
    if any(pattern in user_input for pattern in ["bye", "exit", "goodbye"]):
        print(f"Goodbye, {user_name}! It was a pleasure chatting with you. Have a wonderful day ahead!!")
        break  # Exit the loop to end the program

    # Get and print the chatbot's response
    response = get_response(user_input, user_name)
    print(response)
