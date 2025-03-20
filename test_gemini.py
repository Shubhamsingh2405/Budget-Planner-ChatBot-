import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_gemini_connection():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ Error: Google API key not found in environment variables")
        return
    
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize model
        model = genai.GenerativeModel('gemini-1.5-pro')
        chat = model.start_chat(history=[])
        
        # Test message
        response = chat.send_message("Hello! Can you help me with my budget?")
        print("✅ Gemini API Connection Successful!")
        print("\nTest Response:")
        print(response.text)
        
    except Exception as e:
        print(f"❌ Error connecting to Gemini API: {str(e)}")

if __name__ == "__main__":
    test_gemini_connection() 