import json
import random
import re
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

# Load the intents from the intents.json file
with open('intents.json') as file:
    intents_data = json.load(file)

# Initialize user data
user_name = None

# Function to extract the name from the user input
def extract_name(user_input):
    # If the user just types a single word (likely their name)
    if len(user_input.split()) == 1 and user_input.isalpha():
        return user_input.capitalize()  # Capitalize the name
    
    # Regex patterns to extract name with case insensitivity
    patterns = [
        r"my name is (\w+)",  
        r"I am (\w+)",         
        r"call me (\w+)",     
        r"I'm (\w+)",          
        r"i am (\w+)",        
        r"i'm (\w+)"        
    ]
    
    for pattern in patterns:
        # Case insensitive search
        match = re.search(pattern, user_input, re.IGNORECASE)  
        if match:
            # Capitalize the first letter of the name
            return match.group(1).capitalize()  
    return None

# Function to get response based on detected intent
def get_response(user_input):
    global user_name
    
    # Tokenize user input
    user_input = user_input.lower()
    
    #Extracting name if it isn't set
    if not user_name:
        name = extract_name(user_input)
        if name:
            user_name = name
            return f"Got it! Nice to meet you, {user_name}. What can I do for you today?"
        else:
            return "What should I call you? Please tell me your name."
    
    #Checking if the input matches any patterns for emotion detection or other intents
    for intent in intents_data['intents']:
        for pattern in intent['patterns']:
            if pattern.lower() in user_input:
                #Getting the response and formatting it with the user's name if needed
                response = random.choice(intent['responses'])
                if '{name}' in response:
                    response = response.format(name=user_name)
                return response
    
    #If there is no match then default response returned
    return f"I'm not sure I understand, {user_name}. Can you clarify what you need help with?"

# Main chatbot function to run in terminal
def chatbot():
    print("EduBuddy: Hi! I'm EduBuddy, your friendly assistant. Here's what I can help with:")
    print("""1. Motivation and positivity
2. Study tips and focus strategies
3. Friendly conversations
4. Emotional support
Type 'exit' anytime to leave the chat.""")

    #ask for user's name if unknown
    while True:
        user_input = input("EduBuddy: Before we start, what's your name? ").strip()
        name = extract_name(user_input)
        if name:
            global user_name
            user_name = name
            print(f"EduBuddy: Got it, {user_name}! Nice to meet you!")
            break
        else:
            print("EduBuddy: I didn't catch that. Could you please tell me your name?")

    #staring conversation the actual conversation
    while True:
        user_input = input(f"{user_name}: ").strip()
        
        if user_input.lower() in ["bye", "goodbye", "exit", "see you", "later"]:
            print(f"EduBuddy: Goodbye, {user_name}! Remember, I'm always here to help. Take care!")
            break
        
        response = get_response(user_input)
        print(f"EduBuddy: {response}")

#run the chatbot
if __name__ == "__main__":
    chatbot()
