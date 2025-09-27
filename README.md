FinAI - Your Intelligent Financial Advisor
FinAI is a hyper-personalized, multilingual financial advisor powered by a multi-agent AI system. Built for a hackathon, this project leverages Large Language Models (LLMs) to provide users with intelligent, context-aware insights into their finances through a seamless, voice-enabled interface.

This backend was architected by Nithin G, an Information Science student at JSSSTU, drawing on his experience designing and developing the 3-agent AI system for his college app, AcadMate.

Core Features
Multi-Agent Architecture: The system is built on a robust agentic design:

Profile Agent: The central state manager that holds, protects, and persists all user data.

Expense Agent: Parses and categorizes unstructured transaction text from real-time mobile notifications.

Investment Agent: Acts as an expert financial advisor, using the user's rich profile and live market news to provide personalized, actionable advice.

Automated Expense Tracking: Captures real-time transaction data by parsing notifications from UPI and banking apps (GPay, PhonePe, SMS alerts) on the user's phone.

Persistent User Data: User profiles are securely saved to a local user_profile.json file, ensuring data persistence between sessions.

Multilingual Voice Interface: The backend supports generating responses in both English and Kannada, with a server-side Text-to-Speech (TTS) engine for reliable audio playback.

Tech Stack
Backend: Python, FastAPI

AI & Agents: LangChain, Groq API (for Llama 3.1)

Data Validation: Pydantic

Live News API: GNews

Backend TTS: Google Text-to-Speech (gTTS)

Backend STT: Google Speech Recognition (SpeechRecognition)

Audio Processing: pydub, ffmpeg

Frontend Prototype: HTML, Tailwind CSS, Vanilla JavaScript

Setup & Installation Guide
Follow these steps to get the FinAI backend and frontend running locally.

1. Prerequisites
Python 3.10+

pip and venv

ffmpeg: A critical system dependency for audio processing.

Windows: choco install ffmpeg

macOS: brew install ffmpeg

Linux: sudo apt-get install ffmpeg

2. Clone the Repository
git clone <your-repo-url>
cd FinAI

3. Set Up Python Environment
# Create a virtual environment
python -m venv venv

# Activate it
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

4. Install Dependencies
Install all required Python packages from the requirements.txt file.

pip install -r requirements.txt

5. Add API Keys
You need API keys for the Investment Agent's dynamic data features:

Groq API Key: Get a free key from GroqCloud.

GNews API Key: Get a free key from GNews.

Open investment_agent.py and paste your keys into the placeholder variables at the top.

6. Run the Backend Server
Use uvicorn to run the FastAPI server. The --host 0.0.0.0 flag is essential to make it accessible on your local network, allowing your phone to connect.

uvicorn main:app --reload --host 0.0.0.0

The server will be running at http://<your-local-ip-address>:8000.

7. Set Up the Public Tunnel with ngrok
To receive notifications from your phone, you need a public URL.

# First, authenticate (one-time setup)
ngrok config add-authtoken <YOUR_NGROK_TOKEN>

# Then, start the tunnel
ngrok http 8000

ngrok will provide a public https URL. Use this URL in your phone's automation app (Tasker, Automate, or iOS Shortcuts).

8. Access the UI
Open a browser and go to your server's local address: http://127.0.0.1:8000.

Guide for Frontend Developers
The FinAI backend provides a simple and robust API for integration.

Base URL
http://<your-server-ip>:8000

Core Endpoints
1. Get Investment Advice

Endpoint: POST /ask/investment

Description: The primary endpoint for getting personalized investment suggestions.

Request Body:

{
  "user_query": "What should I do with my extra savings?",
  "language": "en-US" // or "kn-IN"
}

Success Response (200 OK):

{
  "agent_response": "Here is the investment advice in Markdown format..."
}

2. Automated Expense Input

Endpoint: POST /event/expense

Description: Used by the phone automation to feed live transaction data into the system.

Request Body:

{
  "text": "Paid Rs. 150 to Starbucks via GPay"
}

Success Response (200 OK):

{
  "vendor": "Starbucks",
  "amount": 150.0,
  "category": "Food & Drink"
}

3. Profile Management

Get Profile: GET /profile - Returns the complete UserProfile JSON object.

Update Profile: PUT /profile - Updates the user's profile. Send only the fields you want to change.

Request Body:

{
  "risk_tolerance": "high",
  "financial_goals": "Save for a world trip."
}

4. Server-Side Text-to-Speech (TTS)

Endpoint: POST /text-to-speech

Description: Converts the agent's text response into an audio file for reliable playback.

Request Body:

{
  "text": "Here is your investment advice...",
  "language": "en-US" // or "kn-IN"
}

Success Response (200 OK): Returns a raw audio/mpeg file. The frontend should play this using an <audio> tag.
