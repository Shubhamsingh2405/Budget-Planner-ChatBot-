from chatbot import SmartBudgetAIChatbot

def test_chatbot():
    # Initialize the chatbot
    bot = SmartBudgetAIChatbot()
    
    # Test greeting
    response = bot.get_ai_response("Hi there! My name is John")
    print("Response to greeting:", response)
    
    # Test income input
    response = bot.get_ai_response("My monthly income is 50000")
    print("\nResponse to income input:", response)
    
    # Test expense input
    response = bot.get_ai_response("I spend 15000 on rent")
    print("\nResponse to expense (rent):", response)
    
    response = bot.get_ai_response("I also spend 10000 on food")
    print("\nResponse to expense (food):", response)
    
    # Test savings goal
    response = bot.get_ai_response("I want to save 8000 per month")
    print("\nResponse to savings goal:", response)
    
    # Test analysis request
    response = bot.get_ai_response("Can you analyze my budget?")
    print("\nResponse to analysis request:", response)
    
    # Test general question
    response = bot.get_ai_response("What should I do to improve my finances?")
    print("\nResponse to general question:", response)

if __name__ == "__main__":
    test_chatbot() 