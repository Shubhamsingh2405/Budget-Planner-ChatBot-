import requests
import json

def test_llm_api():
    # Using OpenAI-compatible API
    api_url = "https://openrouter.ai/api/v1/chat/completions"
    
    # Test message
    test_message = "Hi, I'm testing the API. Tell me a short joke."
    
    # Headers (no auth needed for basic access)
    headers = {
        "Content-Type": "application/json",
        "HTTP-Referer": "https://financial-chatbot-test.com"  # Just for tracking
    }
    
    # OpenAI-compatible payload
    payload = {
        "model": "openai/gpt-3.5-turbo",  # Using GPT as fallback since Llama requires auth
        "messages": [
            {"role": "system", "content": "You are a helpful financial advisor."},
            {"role": "user", "content": test_message}
        ]
    }
    
    try:
        print("Testing API connection via OpenRouter...")
        print(f"Model: {payload['model']}")
        print("\nSending message:", test_message)
        
        # Make API request
        print("\nSending request...")
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("\nSuccess! Response:")
            result = response.json()
            message = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(message)
        else:
            print("\nError Response:")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"\nNetwork Error: {str(e)}")
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}")

if __name__ == "__main__":
    test_llm_api() 