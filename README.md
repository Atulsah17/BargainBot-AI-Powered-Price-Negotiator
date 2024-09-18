# Negotiation Chatbot API

This is an API that simulates a negotiation chatbot using **FastAPI**, **Google Gemini** for generative AI text responses, and **TextBlob** for sentiment analysis. The chatbot engages in negotiations with a customer, adjusting the price based on sentiment and predefined rules.

## Features
- Conducts negotiations for a Bluetooth speaker starting at $150.
- Provides price reductions based on user sentiment (positive/negative tone).
- Uses fallback generative AI responses when sentiment analysis or specific rules don't apply.
- Handles basic product inquiries about warranty and features.

## Setup and Installation

### Prerequisites
Before running the project, ensure you have the following:
- **Python 3.9+**
- **pip** (Python package manager)
- A **Google Gemini API key** (for generative AI responses)

### Step 1: Clone the Repository
Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/negotiation-chatbot-api.git

Step 2: Install Dependencies

pip install -r requirements.txt

Step 3: Set up Environment Variables
The chatbot uses the Google Gemini API. Set up your API key:

Create a .env file in the project root directory.

Add the following line to your .env file, replacing your_api_key_here with your actual Gemini API key:

GEMINI_API_KEY=your_api_key_here

Step 4: Run the API
Start the FastAPI server using Uvicorn:

uvicorn chatbot:app --reload

The server will be running at http://127.0.0.1:8000

Usage
API Endpoints
1. Health Check (GET /)
Confirms that the API is running.

Example Request: curl -X 'GET' 'http://127.0.0.1:8000/'
{
  "message": "Welcome to the Bluetooth speaker negotiation bot!"
}
2. Negotiate (POST /negotiate)
Processes negotiation messages and responds based on sentiment analysis and predefined rules.

Example Request:curl -X 'POST' \
  'http://127.0.0.1:8000/negotiate' \
  -H 'Content-Type: application/json' \
  -d '{"message": "This seems overpriced, I don’t think it’s worth more than $70."}'
{
  "response": "Your offer of $70 is quite low. The minimum acceptable price is $100. Can we try to meet closer to that?"
}


