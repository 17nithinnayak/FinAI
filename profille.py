import json
from pydantic import BaseModel, Field
from typing import List, Literal
from collections import defaultdict
import os

# We import the Expense model defined in the expense_agent
from expense import Expense

# --- Constants ---
PROFILE_FILE = "user_profile.json"

# --- Data Models ---

class ExpenseSummary(BaseModel):
    category: str
    total_amount: float

# This model is for UPDATING the profile, reflecting the full UI.
class UserProfileUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    age: int | None = None
    gender: Literal["Male", "Female", "Other"] | None = None
    city: str | None = None
    state: str | None = None
    monthly_income: float | None = None
    financial_goals: str | None = None
    risk_tolerance: Literal["low", "medium", "high"] | None = None
    dependents: int | None = None
    liabilities_emi: float | None = None
    investment_interests: str | None = None
    lifestyle_habits: str | None = None


# The main UserProfile, now expanded to match the UI for richer context.
class UserProfile(BaseModel):
    # Essential Information
    name: str = "New User"
    email: str | None = None
    age: int = 25
    gender: Literal["Male", "Female", "Other"] | None = "Male"
    city: str | None = "Bangalore"
    state: str | None = "Karnataka"
    monthly_income: float = 85000.0

    # Financial Information
    financial_goals: str = "Save for house down payment, retirement planning, children education"
    risk_tolerance: Literal["low", "medium", "high"] = "medium"
    dependents: int = 2
    liabilities_emi: float = 15000.0 # e.g., Car loan EMI
    investment_interests: str = "Mutual funds, stocks, FDs"
    lifestyle_habits: str | None = "Dining out twice a week, monthly movie outings"

    # Dynamic Financial State (calculated by the agent)
    total_monthly_spending: float = 0.0 # From expense tracking
    available_savings: float = 0.0
    
    # Raw Data Lists
    expenses: List[Expense] = []
    
# --- The Agent Class ---

class ProfileAgent:
    """
    Manages the user's financial profile state, with persistence to a JSON file.
    """
    def __init__(self):
        self._profile = self._load_profile()
        print(f"🤖 [Profile Agent] Profile for {self._profile.name} loaded successfully.")

    def _load_profile(self) -> UserProfile:
        if os.path.exists(PROFILE_FILE):
            with open(PROFILE_FILE, 'r') as f:
                data = json.load(f)
                return UserProfile(**data)
        else:
            print("🤖 [Profile Agent] No profile file found. Creating a new one.")
            new_profile = UserProfile()
            self._save_profile(new_profile)
            return new_profile

    def _save_profile(self, profile_data: UserProfile):
        with open(PROFILE_FILE, 'w') as f:
            f.write(profile_data.model_dump_json(indent=4))

    def update_profile(self, update_data: UserProfileUpdate):
        profile_dict = self._profile.model_dump()
        update_dict = update_data.model_dump(exclude_unset=True)
        
        profile_dict.update(update_dict)
        self._profile = UserProfile(**profile_dict)
        
        self._recalculate_and_save() # Recalculate savings if income/liabilities change
        print(f"🤖 [Profile Agent] Profile updated for {self._profile.name} and saved.")
        return self._profile

    def add_expense(self, expense: Expense):
        self._profile.expenses.append(expense)
        self._recalculate_and_save()
        print(f"🤖 [Profile Agent] Expense for {expense.vendor} added and profile saved.")

    def _recalculate_and_save(self):
        """CRITICAL: Updated savings calculation including liabilities."""
        self._profile.total_monthly_spending = sum(e.amount for e in self._profile.expenses)
        # Net savings is income minus tracked expenses AND fixed liabilities.
        self._profile.available_savings = self._profile.monthly_income - self._profile.total_monthly_spending - self._profile.liabilities_emi
        self._save_profile(self._profile)

    def get_profile(self) -> UserProfile:
        return self._profile

    def get_expense_summary(self) -> List[ExpenseSummary]:
        summary = defaultdict(float)
        for expense in self._profile.expenses:
            summary[expense.category] += expense.amount
        
        return [
            ExpenseSummary(category=cat, total_amount=total)
            for cat, total in summary.items()
        ]

# --- Singleton Instance ---
profile_agent = ProfileAgent()

