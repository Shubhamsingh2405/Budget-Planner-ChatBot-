import json
import re
import random
from datetime import datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

class SmartBudgetAIChatbot:
    def __init__(self):
        # Configure Gemini API
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("Google API key not found in environment variables")
            
        print("Initializing SmartBudget AI with Gemini...")
        genai.configure(api_key=api_key)
        
        # Initialize Gemini model
        try:
            self.model = genai.GenerativeModel('gemini-1.5-pro')
            self.chat = self.model.start_chat(history=[])
            print("Gemini model initialized successfully")
        except Exception as e:
            print(f"Error initializing Gemini API: {str(e)}")
            print("Falling back to local implementation")
            self.model = None
            self.chat = None
        
        self.user_data = {}
        self.expenses = {}
        self.conversation_history = []
        self.user_name = None
        self.capabilities = [
            "Create and manage monthly budgets 💰",
            "Track expenses by categories 📊",
            "Set and monitor savings goals 🎯",
            "Analyze spending patterns 📈",
            "Provide investment advice 💡",
            "Calculate expense ratios and financial metrics 📊",
            "Suggest tax-saving strategies 💰",
            "Help with debt management 📉"
        ]
        self.last_greeting_time = None
        
        # Financial advice templates - kept for fallback mode
        self.advice_templates = [
            "Based on your expenses, you might want to consider reducing your {category} spending by {percent}% to save more money.",
            "I notice that you're spending {amount} on {category}. That's about {percent}% of your income. The recommended percentage is around {recommended}%.",
            "Looking at your financial data, I suggest focusing on saving more in the {category} category. Try to aim for {goal} per month.",
            "Your {category} expenses seem {status}. Most financial experts recommend keeping it under {recommended}% of your income.",
            "To reach your savings goal of {savings_goal}, consider cutting back on {category} by about {amount} per month.",
            "Great job on managing your {category}! You're spending less than the recommended amount.",
            "To improve your financial health, try the 50/30/20 rule: 50% for needs, 30% for wants, and 20% for savings.",
            "Looking at your spending, I recommend creating an emergency fund of at least 3-6 months of expenses.",
            "Consider automating your savings by setting up automatic transfers to your savings account each month."
        ]
        
        # Response templates - kept for fallback mode
        self.response_templates = {
            "greeting": [
                "👋 Hello {name}! How can I help with your finances today?",
                "Hi there, {name}! Ready to talk about your budget and savings?",
                "Hello {name}! I'm here to help you manage your money better. What can I do for you today?",
                "Hey {name}! Your financial assistant is ready to help. What would you like to do today?"
            ],
            "income_added": [
                "✅ Great! I've recorded your monthly income as ₹{income}.",
                "Thanks! I've noted your income as ₹{income} per month."
            ],
            "expense_added": [
                "📝 Got it! I've added ₹{amount} for {category} to your expenses.",
                "Added: ₹{amount} for {category}. Your total expenses are now ₹{total_expenses}."
            ],
            "savings_goal_added": [
                "🎯 Excellent! Your savings goal is set to ₹{goal} per month.",
                "I've set your monthly savings goal to ₹{goal}. Let's work towards achieving it!"
            ],
            "budget_analysis": [
                "📊 Based on your information:\n• Income: ₹{income}\n• Total Expenses: ₹{total_expenses}\n• Remaining: ₹{remaining}\n\n{advice}",
                "💰 Here's your financial snapshot:\n• Monthly Income: ₹{income}\n• Total Expenses: ₹{total_expenses}\n• Available for Savings: ₹{remaining}\n\n{advice}"
            ],
            "general": [
                "I'm here to help with your budget! You can tell me about your income, expenses, or savings goals.",
                "Need help with something specific? You can ask me about budget analysis, expense tracking, or savings advice.",
                "Feel free to share more details about your financial situation so I can provide better advice.",
                "Is there anything specific about your finances you'd like to discuss today?"
            ]
        }

    def get_ai_response(self, user_input):
        if self.model and self.chat:
            try:
                # Add financial context to the prompt
                context = self.format_conversation_history()
                financial_context = self.format_financial_context()
                
                prompt = f"""
                You are a friendly and casual financial chatbot named Fin. Act like a helpful friend who's good with money, not a formal advisor. Keep these points in mind:

                Your Personality:
                - Super friendly and casual - use "hey", "cool", etc.
                - Chat like a friend texting
                - Keep responses short and sweet (2-3 sentences max per point)
                - Use everyday language, avoid financial jargon
                - Be encouraging and positive
                - Use emojis naturally (1-2 per message)
                - Share quick, practical money tips
                
                When giving financial advice:
                - Break it down simply
                - Use real-life examples
                - Give one main tip at a time
                - Keep numbers simple (round figures)
                - Use ₹ for money values
                - Be encouraging, not judgmental

                Financial Context:
                {financial_context}

                Previous Conversation:
                {context}

                User's message: {user_input}

                Remember:
                - Chat casually like a friend
                - Keep it short and simple
                - Be positive and encouraging
                - Use natural, conversational language
                - If topic isn't about money, gently bring it back to finances in a friendly way
                - Never sound like a formal advisor or AI
                """
                
                response = self.chat.send_message(prompt)
                return response.text
            except Exception as e:
                print(f"Error getting Gemini response: {str(e)}")
                return self.generate_contextual_response(user_input)
        else:
            return self.generate_contextual_response(user_input)

    def format_conversation_history(self):
        if not self.conversation_history:
            return "This is the start of the conversation."
        
        formatted_history = []
        for entry in self.conversation_history[-5:]:  # Keep last 5 exchanges for context
            formatted_history.append(f"{entry['role']}: {entry['content']}")
        return "\n".join(formatted_history)

    def format_financial_context(self):
        if not self.user_data and not self.expenses:
            return "No financial data available yet."
        
        context = []
        if self.user_data:
            context.append("User Financial Profile:")
            for key, value in self.user_data.items():
                if key == 'income':
                    context.append(f"- Monthly Income: ₹{value:,.2f}")
                elif key == 'savings_goal':
                    context.append(f"- Savings Goal: ₹{value:,.2f}")
                else:
                    context.append(f"- {key.title()}: {value}")
        
        if self.expenses:
            context.append("\nExpense Categories:")
            for category, amount in self.expenses.items():
                context.append(f"- {category}: ₹{amount:,.2f}")
        
        return "\n".join(context)

    def generate_contextual_response(self, user_input):
        # This is the fallback local implementation
        # Check if we need to respond about specific financial topics
        
        # If user mentioned savings goal in this message
        savings_patterns = [
            r'(?i)(?:save|saving|savings|goal)\s+(?:rs\.?|₹)?\s*(\d+(?:,\d+)*(?:\.\d+)?)',
            r'(?i)(?:want to|wanna|going to|plan to)\s+save\s+(?:rs\.?|₹)?\s*(\d+(?:,\d+)*(?:\.\d+)?)'
        ]
        
        for pattern in savings_patterns:
            savings_match = re.search(pattern, user_input)
            if savings_match:
                try:
                    goal = float(savings_match.group(1).replace(",", ""))
                    self.user_data["savings_goal"] = goal
                    
                    template = random.choice(self.response_templates["savings_goal_added"])
                    return template.format(goal=f"{goal:,.0f}")
                except (ValueError, IndexError):
                    pass
        
        # If user added income recently
        if "income" in self.user_data and len(self.conversation_history) < 3:
            template = random.choice(self.response_templates["income_added"])
            return template.format(income=f"{self.user_data['income']:,.0f}")
        
        # If user added expense
        expense_pattern = r'(?i)(?:spend|spent|spending|pay|paying|paid|expense|expenses|cost|costs)\s+(?:rs\.?|₹)?\s*(\d+(?:,\d+)*(?:\.\d+)?)\s+(?:on|for|in)\s+([a-zA-Z\s]+)'
        expense_match = re.search(expense_pattern, user_input)
        if expense_match:
            amount = float(expense_match.group(1).replace(",", ""))
            category = expense_match.group(2).strip().lower()
            total_expenses = sum(self.expenses.values()) if self.expenses else 0
            
            template = random.choice(self.response_templates["expense_added"])
            return template.format(amount=f"{amount:,.0f}", category=category, total_expenses=f"{total_expenses:,.0f}")
        
        # If user asks for budget analysis
        analysis_keywords = ["analyze", "analysis", "how am i doing", "budget", "review", "overview", "summary", "status"]
        if any(keyword in user_input.lower() for keyword in analysis_keywords) and "income" in self.user_data:
            income = self.user_data["income"]
            total_expenses = sum(self.expenses.values()) if self.expenses else 0
            remaining = income - total_expenses
            
            # Generate advice
            if self.expenses:
                try:
                    highest_category = max(self.expenses.items(), key=lambda x: x[1])
                    highest_percent = (highest_category[1] / income) * 100
                    
                    advice_template = random.choice(self.advice_templates)
                    advice = advice_template.format(
                        category=highest_category[0],
                        amount=f"{highest_category[1]:,.0f}",
                        percent=f"{highest_percent:.1f}",
                        recommended="15-20",
                        status="high" if highest_percent > 30 else "reasonable",
                        goal=f"{income * 0.2:,.0f}",
                        savings_goal=f"{self.user_data.get('savings_goal', income * 0.2):,.0f}"
                    )
                except (ValueError, TypeError) as e:
                    advice = "Consider tracking your expenses by category to get more specific advice."
            else:
                advice = "Consider tracking your expenses by category to get more specific advice."
            
            template = random.choice(self.response_templates["budget_analysis"])
            return template.format(
                income=f"{income:,.0f}",
                total_expenses=f"{total_expenses:,.0f}",
                remaining=f"{remaining:,.0f}",
                advice=advice
            )
        
        # Default to general advice
        if self.user_name:
            # Personalized response if we know the user's name
            greeting = f"Hi {self.user_name}! "
            return greeting + random.choice(self.response_templates["general"])
        else:
            return random.choice(self.response_templates["general"])
            
    def extract_financial_info(self, text):
        # Extract income
        income_pattern = r'(?i)(?:income|earn|salary|make|making)(?:\s+is|\s+of)?\s+(?:rs\.?|₹)?\s*(\d+(?:,\d+)*(?:\.\d+)?)'
        income_match = re.search(income_pattern, text)
        if income_match:
            try:
                income_value = income_match.group(1).replace(",", "")
                self.user_data["income"] = float(income_value)
            except ValueError:
                pass

        # Extract expenses
        expense_pattern = r'(?i)(?:spend|spent|spending|pay|paying|paid|expense|expenses|cost|costs)\s+(?:rs\.?|₹)?\s*(\d+(?:,\d+)*(?:\.\d+)?)\s+(?:on|for|in)\s+([a-zA-Z\s]+)'
        expense_matches = re.finditer(expense_pattern, text)
        for match in expense_matches:
            try:
                amount = float(match.group(1).replace(",", ""))
                category = match.group(2).strip().lower()
                self.expenses[category] = amount
            except ValueError:
                pass

        # Extract savings goal
        savings_patterns = [
            r'(?i)(?:save|saving|savings|goal)\s+(?:rs\.?|₹)?\s*(\d+(?:,\d+)*(?:\.\d+)?)',
            r'(?i)(?:want to|wanna|going to|plan to)\s+save\s+(?:rs\.?|₹)?\s*(\d+(?:,\d+)*(?:\.\d+)?)'
        ]
        
        for pattern in savings_patterns:
            savings_match = re.search(pattern, text)
            if savings_match:
                try:
                    savings_value = savings_match.group(1).replace(",", "")
                    self.user_data["savings_goal"] = float(savings_value)
                    break  # Stop after first match
                except ValueError:
                    pass
                
        # Extract user name if not already set
        if not self.user_name:
            name_patterns = [
                r'(?i)(?:my name is|I am|I\'m) ([A-Za-z]+)',
                r'(?i)(?:call me) ([A-Za-z]+)',
                r'(?i)^(?:I\'m|I am) ([A-Za-z]+)'
            ]
            
            for pattern in name_patterns:
                name_match = re.search(pattern, text)
                if name_match:
                    self.user_name = name_match.group(1).capitalize()
                    break

    def handle_greeting(self, user_input):
        greetings = ['hi', 'hello', 'hey', 'hola', 'greetings']
        current_time = datetime.now()
        if any(greeting in user_input.lower() for greeting in greetings):
            if self.last_greeting_time is None or (current_time - self.last_greeting_time).seconds > 300:
                self.last_greeting_time = current_time
                responses = [
                    "👋 Hi there! I'm your AI financial buddy. Want to know what I can do? Just ask 'what can you do?' Or we can start budgeting - what's your name?",
                    "Hello! I'm here to help with your finances. Ask me 'what can you do?' to learn more, or we can get started - what's your name?",
                    "Hey! 😊 I'm your personal finance assistant. Want to see my capabilities? Ask 'what can you do?' Or let's begin - what's your name?",
                    "Hi! Ready to manage your finances better? Ask me 'what can you do?' to learn more, or we can start right away - what's your name?"
                ]
                return random.choice(responses)
            return "I'm here to help! Just let me know what you need."
        return None

    def handle_capabilities(self, user_input):
        capability_triggers = ['what can you do', 'your capabilities', 'help me', 'what do you do', 'how can you help']
        if any(trigger in user_input.lower() for trigger in capability_triggers):
            response = "I'm your personal finance assistant! Here's what I can do for you:\n\n"
            for capability in self.capabilities:
                response += f"• {capability}\n"
            response += "\nReady to get started? Just tell me your name! 😊"
            return response
        return None

    def get_greeting(self):
        greetings = [
            "Hey there! 👋 I'm your personal finance buddy. What's your name?",
            "Hi! I'm excited to help you manage your finances better. What should I call you?",
            "Welcome! I'm your AI financial assistant. Before we start, could you tell me your name?",
            "Hello! Let's work on your budget together. First, what's your name?"
        ]
        return random.choice(greetings)

    def get_income_question(self):
        questions = [
            f"Thanks {self.user_name}! Let's start with your monthly income - how much do you earn?",
            f"Great to meet you, {self.user_name}! To help you better, could you tell me your monthly income?",
            f"Alright {self.user_name}! What's your monthly income? This will help me understand your financial situation.",
            f"Perfect, {self.user_name}! How much money do you make each month?"
        ]
        return random.choice(questions)

    def get_expense_prompt(self):
        prompts = [
            f"Now {self.user_name}, tell me about your expenses. You can add any category you want! For example, say something like 'I spend 5000 on groceries' or '3000 for gaming'.",
            f"Let's talk about where your money goes, {self.user_name}. Just tell me naturally about any expense category - could be anything from 'coffee' to 'pet care'!",
            f"What kind of things do you spend money on, {self.user_name}? You can tell me about any category - like '2000 on movies' or '6000 for hobbies'.",
            f"Time to track your spending, {self.user_name}! Share your expenses in any categories you like - maybe start with your biggest expense?"
        ]
        return random.choice(prompts)

    def get_expense_acknowledgment(self, category, amount):
        acks = [
            f"Got it! ₹{amount:,.2f} for {category}. What other expenses would you like to add?",
            f"Added ₹{amount:,.2f} for {category}. Tell me about another expense, or say 'done' when you're finished!",
            f"Noted ₹{amount:,.2f} for {category}. What else do you spend money on?",
            f"I've recorded ₹{amount:,.2f} for {category}. Keep going! Or say 'done' if that's all."
        ]
        return random.choice(acks)

    def get_savings_question(self):
        questions = [
            f"Great job listing your expenses, {self.user_name}! How much would you like to save each month?",
            f"Now let's set a savings target, {self.user_name}. How much would you like to set aside monthly?",
            f"Time to think about savings, {self.user_name}! What's your monthly savings goal?",
            f"Let's plan your savings, {self.user_name}. How much do you want to save each month?"
        ]
        return random.choice(questions)

    def extract_number(self, text):
        numbers = re.findall(r'\d+(?:,\d+)*(?:\.\d+)?', text)
        if numbers:
            return float(numbers[0].replace(',', ''))
        return None

    def extract_category(self, text):
        # Remove common expense-related words and amounts
        text = re.sub(r'\d+(?:,\d+)*(?:\.\d+)?', '', text)
        text = text.lower()
        words_to_remove = ['spend', 'spent', 'spending', 'pay', 'paid', 'paying', 'cost', 'costs', 'costing',
                          'rupees', 'rs', 'inr', '₹', 'on', 'for', 'in', 'my', 'i', 'around', 'about']
        
        for word in words_to_remove:
            text = text.replace(word, '')
        
        # Clean up the remaining text
        category = text.strip()
        if category:
            # Take the last meaningful word/phrase as the category
            category_parts = [part for part in category.split() if len(part) > 1]
            if category_parts:
                return ' '.join(category_parts)
        return None

    def process_input(self, user_input):
        # Extract name if not set
        if not self.user_name:
            name_match = re.search(r'my name is (\w+)', user_input.lower())
            if name_match:
                self.user_name = name_match.group(1).title()

        # Get AI response
        return self.get_ai_response(user_input)
