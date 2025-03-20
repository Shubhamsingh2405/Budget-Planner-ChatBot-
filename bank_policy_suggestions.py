from web_search import get_financial_advice

class BankPolicySuggestions:
    def suggest_policies(self, savings_goal):
        try:
            # Get real-time banking product recommendations
            search_query = f"best savings accounts and banking products for {savings_goal} monthly savings india"
            banking_advice = get_financial_advice(search_query)
            
            response = "🏦 Banking Recommendations:\n\n"
            response += banking_advice
            
            # Get additional tax saving suggestions if applicable
            if savings_goal >= 10000:
                tax_query = "best tax saving investment options india"
                tax_advice = get_financial_advice(tax_query)
                response += "\n\n💰 Tax Saving Options:\n"
                response += tax_advice
            
            return response
        except Exception as e:
            # Fallback suggestions if web search fails
            if savings_goal < 5000:
                return """• Consider opening a high-interest savings account
• Look into recurring deposit schemes
• Check for zero-balance account options
• Use UPI and digital banking for cashback benefits
• Compare different banks' savings account interest rates"""
            elif savings_goal < 20000:
                return """• Explore fixed deposit options with higher interest rates
• Consider post office savings schemes
• Look into mutual fund SIP options
• Check for special banking programs for regular savers
• Compare different banks' premium savings accounts"""
            else:
                return """• Consider premium banking services for higher value accounts
• Look into wealth management services
• Explore multi-deposit schemes
• Check for relationship banking benefits
• Compare different banks' investment advisory services"""
