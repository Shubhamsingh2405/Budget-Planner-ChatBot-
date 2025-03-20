import json
from web_search import get_financial_advice

class FinancialAnalysis:
    def calculate_total_expenses(self, expenses):
        return sum(expenses.values())

    def calculate_remaining_balance(self, income, total_expenses):
        return income - total_expenses

    def get_expense_breakdown(self, expenses, income):
        # Calculate percentage of income for each expense
        expense_percentages = {}
        for category, amount in expenses.items():
            percentage = (amount / income) * 100
            expense_percentages[category] = percentage
        return expense_percentages

    def get_50_30_20_analysis(self, income, total_expenses, savings_goal):
        # Calculate ideal allocations based on 50/30/20 rule
        needs = income * 0.5  # 50% for needs
        wants = income * 0.3  # 30% for wants
        savings = income * 0.2  # 20% for savings
        
        return {
            "needs": needs,
            "wants": wants,
            "savings": savings
        }

    def suggest_savings(self, remaining_balance, savings_goal):
        try:
            # Get personalized financial advice from the web
            search_query = f"best savings strategies for monthly savings goal of {savings_goal} rupees india"
            financial_advice = get_financial_advice(search_query)
            
            if remaining_balance < savings_goal:
                deficit = savings_goal - remaining_balance
                search_query = f"how to reduce monthly expenses to save {deficit} rupees india"
                expense_reduction_tips = get_financial_advice(search_query)
                
                response = "📊 Savings Analysis:\n\n"
                response += f"You're currently ₹{deficit:,.2f} short of your savings goal.\n\n"
                response += "💡 Personalized Recommendations:\n"
                response += financial_advice + "\n\n"
                response += "✂️ Expense Reduction Tips:\n"
                response += expense_reduction_tips
            else:
                surplus = remaining_balance - savings_goal
                search_query = f"best investment options for {surplus} rupees monthly surplus india"
                investment_advice = get_financial_advice(search_query)
                
                response = "📈 Investment Opportunities:\n\n"
                response += f"Great! You have a surplus of ₹{surplus:,.2f} after meeting your savings goal.\n\n"
                response += "💰 Investment Recommendations:\n"
                response += financial_advice + "\n\n"
                response += "🎯 Additional Investment Options:\n"
                response += investment_advice
            
            return response
        except Exception as e:
            # Fallback to basic recommendations if web search fails
            if remaining_balance < savings_goal:
                return "Consider reducing discretionary expenses and look for additional income sources to meet your savings goal."
            else:
                return "You're on track with your savings goal! Consider investing the surplus in diversified portfolios."
