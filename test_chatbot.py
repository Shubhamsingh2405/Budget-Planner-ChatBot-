import os
from dotenv import load_dotenv
import google.generativeai as genai
from chatbot import SmartBudgetAIChatbot

def test_chatbot():
    # Initialize the chatbot
    chatbot = SmartBudgetAIChatbot()
    
    # Test scenarios
    test_cases = [
        {
            "scenario": "Initial Greeting",
            "input": "Hello! I need help with my budget."
        },
        {
            "scenario": "Income Information",
            "input": "I earn ₹50,000 per month from my job."
        },
        {
            "scenario": "Expense Tracking",
            "input": "My monthly expenses are: Rent ₹15,000, Food ₹8,000, Transport ₹3,000"
        },
        {
            "scenario": "Savings Goal",
            "input": "I want to save ₹20,000 per month for a house down payment."
        },
        {
            "scenario": "Financial Advice",
            "input": "Can you analyze my spending and give me advice?"
        }
    ]
    
    print("🤖 Starting Chatbot Tests...\n")
    
    for test in test_cases:
        print(f"📝 Testing: {test['scenario']}")
        print(f"User: {test['input']}")
        
        try:
            response = chatbot.process_input(test['input'])
            print(f"Bot: {response}\n")
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")
        
        print("-" * 50 + "\n")

if __name__ == "__main__":
    test_chatbot() 