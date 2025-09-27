import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Literal

# SECURE: API key is no longer hardcoded

class Expense(BaseModel):
    vendor: str = Field(...)
    amount: float = Field(...)
    category: Literal["Food & Drink", "Transportation", "Shopping", "Bills & Utilities", "Entertainment", "Groceries", "Health & Wellness", "Other"]

def parse_expense_from_text(text: str) -> Expense:
    llm = ChatGroq(temperature=0, model_name="llama-3.1-8b-instant")
    structured_llm = llm.with_structured_output(Expense)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert text-parsing AI. Your sole job is to analyze a given text,
                extract the vendor name, the expense amount, and classify it into one of the
                provided categories.
                - The vendor is the place where the money was spent (e.g., 'Zomato', 'Swiggy', 'IndianOil').
                - The amount is the primary transaction value. Ignore any mention of account balances.
                - For UPI transactions, the vendor is often part of the UPI ID (e.g., 'swiggy@okhdfcbank').
                - Always return the data in the specified JSON format."""
            ),
            (
                "human",
                "Please parse the following text: '{text_input}'"
            ),
        ]
    )
    chain = prompt | structured_llm
    return chain.invoke({"text_input": text})

