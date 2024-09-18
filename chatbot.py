from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from textblob import TextBlob
import logging

# Initialize FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the initial offer and negotiation rules
INITIAL_PROMPT = (
    "Welcome to our negotiation chatbot! We are currently offering a high-quality Bluetooth speaker for $150. "
    "Feel free to make an offer, and we can discuss the price. "
    "The minimum acceptable offer is $100. If you are polite, we may offer a better deal. "
    "Let's start the negotiation!"
)

# Sentiment analysis function
def analyze_sentiment(user_input):
    try:
        analysis = TextBlob(user_input)
        return analysis.sentiment.polarity
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {e}")
        return 0.0  # Default to neutral if analysis fails

# Function to handle basic enquiries
def handle_basic_enquiry(user_input):
    lower_input = user_input.lower()
    if "warranty" in lower_input:
        return "The Bluetooth speaker comes with a 1-year warranty."
    if "features" in lower_input or "tell me about" in lower_input or "what can you tell me" in lower_input:
        return "This Bluetooth speaker features high-quality sound, Bluetooth 5.0 connectivity, a 12-hour battery life, and water resistance."
    return None  # No basic enquiry detected

# Adjust sentiment threshold handling
def determine_response_based_on_sentiment(sentiment_score, user_input):
    # Handle high sentiment (positive tone)
    if sentiment_score > 0.2:
        if "120" in user_input or "one hundred twenty" in user_input.lower():
            return "I appreciate your offer of $120. I can accept it, and we have a deal!"
        return "Thank you for your positive tone! I can offer you the speaker for $130."
    
    # Handle low sentiment (negative tone)
    elif sentiment_score < -0.2:
        return "I understand you're not satisfied, but $150 is the lowest we can go. Let me know if you'd like to proceed."
    
    # Neutral sentiment or unhandled case
    else:
        if "70" in user_input or "seventy" in user_input.lower():
            return "Your offer of $70 is quite low. The minimum acceptable price is $100. Can we try to meet closer to that?"
        if "120" in user_input or "one hundred twenty" in user_input.lower():
            return "I can meet you at $130. It's a great deal for this speaker!"
        elif "100" in user_input or "one hundred" in user_input.lower():
            return "Your offer of $100 is acceptable. Let's finalize the deal!"
        return None  # No specific price-based logic matched

# Clean AI response (if needed for fallback)
def clean_response(response_text):
    return response_text.replace("\n", " ").strip()

# Base model for user input
class UserInput(BaseModel):
    message: str

# API root to check if chatbot is running
@app.get("/")
def root():
    return {"message": "Welcome to the Bluetooth speaker negotiation bot!"}

# POST endpoint for handling negotiations
@app.post("/negotiate")
async def negotiate(user_input: UserInput):
    # Initialize conversation history at the start of a negotiation
    conversation_history = []

    try:
        # Start conversation if history is empty
        if not conversation_history:
            conversation_history.append({"role": "model", "parts": [{"text": INITIAL_PROMPT}]})

        # Check for basic enquiries
        basic_response = handle_basic_enquiry(user_input.message)
        if basic_response:
            return {"response": basic_response}

        # Analyze sentiment of the user's input
        sentiment_score = analyze_sentiment(user_input.message)

        # Get response based on sentiment analysis
        bot_response = determine_response_based_on_sentiment(sentiment_score, user_input.message)

        if not bot_response:
            # Fallback response if no predefined rules match
            bot_response = "I’m not sure how to respond to that, but the speaker is $130. Can we negotiate further?"

        # Update conversation history with the user's message and bot's response
        conversation_history.append({"role": "user", "parts": [{"text": user_input.message}]})
        conversation_history.append({"role": "model", "parts": [{"text": bot_response}]})

        # Return bot's response
        return {"response": bot_response}

    except Exception as e:
        logger.error(f"Negotiation failed: {e}")
        raise HTTPException(status_code=500, detail="Negotiation process failed.")
