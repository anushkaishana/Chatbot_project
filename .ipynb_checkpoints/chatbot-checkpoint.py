import json
import random
import nltk
from nltk.tokenize import word_tokenize;

# Download necessary NLTK resources
nltk.download('punkt')

# Load the intents from the intents.json file
with open('intents.json') as file:
    intents_data = json.load(file)

# Function to detect emotions from user input based on keywords
def detect_emotion(user_input):
    # Define a set of keywords for different emotions
    emotions = {
        "sad": ["sad", "down", "depressed", "blue", "unhappy", "low", "crying", "heartbroken"],
        "stressed": ["stressed", "anxious", "worried", "overwhelmed", "nervous", "too much work", "pressure", "can't handle it"],
        "unmotivated": ["unmotivated", "lazy", "tired", "unfocused", "bored", "lack of energy"],
        "happy": ["happy", "excited", "joyful", "grateful", "content"]
    }
    
    # Tokenize the user input into words
    tokens = word_tokenize(user_input.lower())
    
    # Check if any keyword from emotions matches the user input
    for emotion, keywords in emotions.items():
        if any(keyword in tokens for keyword in keywords):
            return emotion
    
    # If no match, return None
    return None

# Function to get response based on detected intent
def get_response(user_input):
    # Tokenize user input
    user_input = user_input.lower()
    
    # First, check if the input matches any patterns for emotion detection
    emotion = detect_emotion(user_input)
    
    if emotion:
        for intent in intents_data['intents']:
            if intent['tag'] == emotion:
                return random.choice(intent['responses'])
    
    # If no emotion is detected, try matching general patterns like greetings, study help, etc.
    for intent in intents_data['intents']:
        for pattern in intent['patterns']:
            if pattern.lower() in user_input:
                return random.choice(intent['responses'])
    
    # If no pattern matches, return a default response
    return "I'm not sure I understand. Can you clarify?"

# Main chatbot function to run in terminal
def chatbot():
    print("EduBuddy: Hi! I'm EduBuddy, your friendly assistant. Here's what I can help with:")
    print("""
    1. Motivation and positivity
    2. Study tips and focus strategies
    3. Friendly conversations
    4. Emotional support
    Type 'exit' anytime to leave the chat.
    """)
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["bye", "goodbye", "exit", "see you", "later"]:
            print("EduBuddy: Goodbye! Remember, I'm always here to help. Take care!")
            break
        
        response = get_response(user_input)
        print(f"EduBuddy: {response}")

# Run the chatbot
if __name__ == "__main__":
    chatbot()
