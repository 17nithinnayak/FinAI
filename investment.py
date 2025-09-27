import os
import requests
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import List
from profille import UserProfile
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

GNEWS_API_KEY = os.environ.get("GNEWS_API_KEY")
if not GNEWS_API_KEY:
    raise ValueError("GNEWS_API_KEY not found in environment variables")

class MarketDataItem(BaseModel):
    title: str
    description: str
    url: str

def fetch_market_data() -> List[MarketDataItem]:
    print("🤖 [Data Fetcher] Calling live GNews API for market sentiment...")
    static_fallback_data = [MarketDataItem(title="NIFTY 50 hits all-time high", description="...", url="#")]
    try:
        response = requests.get(
            f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&token={GNEWS_API_KEY}",
            timeout=10 
        )
        response.raise_for_status()
        articles = response.json().get("articles", [])
        if not articles: return static_fallback_data
        print("✅ [Data Fetcher] Live data fetched successfully.")
        return [MarketDataItem(**article) for article in articles[:5]]
    except requests.exceptions.RequestException as e:
        print(f"🚨 [Data Fetcher] API call failed: {e}. Falling back.")
        return static_fallback_data

def get_investment_suggestion(user_profile: UserProfile, user_query: str, language_name: str = 'English') -> str:
    print(f"🤖 [Investment Agent] Initiating...")
    
    market_data = fetch_market_data()
    market_data_str = "\n".join([f"- {item.title} (Source: {item.url})" for item in market_data])

    # This prompt is now always in English for quality and consistency
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", 
         "You are FinBot, an expert AI financial advisor for Indian users. Your tone is helpful and clear. "
         "You MUST base your analysis *only* on the provided real-time market news. "
         "Cite the 'Source' URL for any news you reference. Format your response using Markdown."),
        ("human", 
         "My profile: {name}, {age} years old, {risk_tolerance} risk tolerance. "
         "My savings this month are Rs. {available_savings:,.2f}. "
         "My financial goals are: {financial_goals}. "
         "Latest market news:\n{market_data}\n\n"
         "My question: {user_query}")
    ])

    chat = ChatGroq(temperature=0.1, model_name="llama-3.1-8b-instant")
    chain = prompt_template | chat | StrOutputParser()

    print("🤖 [Investment Agent] Generating hyper-personalized response in English...")
    
    english_response = chain.invoke({
        "name": user_profile.name,
        "age": user_profile.age,
        "risk_tolerance": user_profile.risk_tolerance,
        "available_savings": user_profile.available_savings,
        "financial_goals": user_profile.financial_goals,
        "market_data": market_data_str,
        "user_query": user_query
    })
    
    # --- DEDICATED TRANSLATION STEP ---
    if language_name == "Kannada":
        print("🤖 [Investment Agent] Translating response to Kannada...")
        translation_prompt = ChatPromptTemplate.from_template(
            "Translate the following financial advice text accurately into Kannada. Preserve the markdown formatting, including links and bold text.\n\n{text_to_translate}"
        )
        translation_chain = translation_prompt | chat | StrOutputParser()
        kannada_response = translation_chain.invoke({"text_to_translate": english_response})
        print("✅ [Investment Agent] Translation complete.")
        return kannada_response

    print("✅ [Investment Agent] English response ready.")
    return english_response

