from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.responses import FileResponse
import os
from typing import Optional

# --- Agent Imports ---
# This version now re-includes the Expense Agent for our live data pipeline
from investment import get_investment_suggestion
from profille import profile_agent, UserProfile, UserProfileUpdate
from expense import parse_expense_from_text, Expense
from dotenv import load_dotenv
load_dotenv()
# --- Language Code to Name Mapping ---
LANGUAGE_MAP = { "en-US": "English", "kn-IN": "Kannada" }

# --- API Data Models ---
class InvestmentQuery(BaseModel):
    user_query: str
    language: Optional[str] = 'en-US'

class ExpenseText(BaseModel):
    text: str

# --- API Setup ---
app = FastAPI(title="Aarthik Mitra API - Live Automation", version="8.0.0")

# --- Frontend Serving ---
@app.get("/", response_class=FileResponse, tags=["Frontend"])
async def read_index():
    return FileResponse("frontend/index.html")

# === THE LIVE DATA ENDPOINT ===
# This is the target for your iPhone Shortcut
@app.post("/event/expense", response_model=Expense, tags=["Events"])
def process_expense_event(expense_data: ExpenseText):
    """
    Receives raw text from a phone's SMS notification (via ngrok),
    parses it using the Expense Agent, and adds it to the user's profile.
    """
    try:
        # Step 1: The Expense Agent parses the raw text
        parsed_expense = parse_expense_from_text(expense_data.text)
        
        # Step 2: The result is sent to the Profile Agent to be saved
        profile_agent.add_expense(parsed_expense)
        
        return parsed_expense
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse expense: {str(e)}")

# === Investment Agent Endpoint ===
@app.post("/ask/investment", tags=["Agents"])
def ask_investment_agent(query: InvestmentQuery):
    try:
        current_profile = profile_agent.get_profile()
        language_name = LANGUAGE_MAP.get(query.language, "English")
        suggestion = get_investment_suggestion(current_profile, query.user_query, language_name)
        return {"agent_response": suggestion}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === Profile Management Endpoints ---
@app.get("/profile", response_model=UserProfile, tags=["Profile"])
def get_user_profile():
    return profile_agent.get_profile()

@app.put("/profile", response_model=UserProfile, tags=["Profile"])
def update_user_profile(update_data: UserProfileUpdate):
    return profile_agent.update_profile(update_data)

