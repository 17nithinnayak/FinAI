from pydantic import BaseModel
from collections import defaultdict

# Import the core data models we need from the profile agent
from profille import UserProfile, ExpenseSummary

# --- Data Models for the Savings Dashboard API Response ---

class SavingsBarData(BaseModel):
    """Data specifically for a visual savings bar."""
    monthly_income: float
    total_expenses: float  # This will include both tracked spending and fixed liabilities
    net_savings: float

class SavingsAnalysis(BaseModel):
    """Data for the 'Current vs Potential' insight card."""
    current_monthly_savings: float
    potential_monthly_savings: float  # Based on the 50/30/20 rule
    insight: str  # A human-readable text insight

class SavingsDashboardData(BaseModel):
    """The complete data payload for the savings dashboard section."""
    savings_bar: SavingsBarData
    spending_chart: list[ExpenseSummary]
    savings_analysis: SavingsAnalysis

# --- The Agent Class ---

class SavingsAgent:
    """
    A stateless agent that analyzes a user's profile to provide savings insights.
    It doesn't hold data itself; it just performs calculations.
    """
    def analyze_and_get_dashboard_data(self, profile: UserProfile) -> SavingsDashboardData:
        """
        Takes a user profile and returns a structured object for the dashboard.
        """
        print("🤖 [Savings Agent] Analyzing profile for dashboard insights...")

        # 1. Calculate data for the Savings Bar
        # Total expenses = what they've spent so far + fixed monthly EMIs
        total_monthly_expenses = profile.total_monthly_spending + profile.liabilities_emi
        
        savings_bar_data = SavingsBarData(
            monthly_income=profile.monthly_income,
            total_expenses=total_monthly_expenses,
            net_savings=profile.available_savings
        )

        # 2. Calculate data for the Spending Chart (Pie Chart)
        # We can reuse the same logic from the ProfileAgent for consistency.
        summary = defaultdict(float)
        for expense in profile.expenses:
            summary[expense.category] += expense.amount
        
        spending_chart_data = [
            ExpenseSummary(category=cat, total_amount=total)
            for cat, total in summary.items()
        ]

        # 3. Perform Savings Analysis (Current vs. Potential)
        # We'll use the 50/30/20 rule to calculate potential savings.
        potential_savings = profile.monthly_income * 0.20
        
        insight_text = ""
        if profile.available_savings < 0:
             insight_text = (
                f"Based on your income, a 20% savings goal would be ₹{potential_savings:,.0f}. "
                "Currently, your expenses are higher than your income. Let's work on tracking your spending to find areas to save!"
            )
        elif profile.available_savings < potential_savings:
            insight_text = (
                f"You're saving well! Based on the 50/30/20 rule, you have the potential to save up to "
                f"₹{potential_savings:,.0f} each month. You're on the right track!"
            )
        else:
            insight_text = (
                f"Fantastic! You're currently saving ₹{profile.available_savings:,.0f} per month, "
                f"which exceeds the recommended 20% savings goal of ₹{potential_savings:,.0f}. Keep up the great work!"
            )
            
        savings_analysis_data = SavingsAnalysis(
            current_monthly_savings=profile.available_savings,
            potential_monthly_savings=potential_savings,
            insight=insight_text
        )

        # 4. Assemble the final dashboard data object
        return SavingsDashboardData(
            savings_bar=savings_bar_data,
            spending_chart=spending_chart_data,
            savings_analysis=savings_analysis_data
        )

# --- Singleton Instance ---
# We create a single instance for the app to use.
savings_agent = SavingsAgent()
