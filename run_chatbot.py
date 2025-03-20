from chatbot import SmartBudgetAIChatbot

def main():
    chatbot = SmartBudgetAIChatbot()
    print("\n=== Smart Budget AI Chatbot ===\n")
    print("Type 'exit' or 'quit' to end the conversation\n")
    
    # Initial greeting
    print("Bot:", chatbot.process_input(""))
    
    while True:
        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for exit command
            if user_input.lower() in ['exit', 'quit']:
                print("\nBot: Thanks for using Smart Budget AI! Goodbye! 👋")
                break
            
            # Process input and get response
            response = chatbot.process_input(user_input)
            print("\nBot:", response)
            
        except KeyboardInterrupt:
            print("\n\nBot: Goodbye! Have a great day! 👋")
            break
        except Exception as e:
            print("\nBot: Oops! Something went wrong. Let's try again!")

if __name__ == "__main__":
    main() 