from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# -------------------------------
# Dynamic Controls by Age
# -------------------------------
def get_temperature(age):
    if age <= 10: return 0.2
    elif age <= 15: return 0.3
    elif age <= 20: return 0.5
    elif age <= 30: return 0.6
    elif age <= 35: return 0.5
    elif age <= 40: return 0.4
    elif age <= 50: return 0.4
    elif age <= 65: return 0.3
    else: return 0.2

def get_max_tokens(age):
    if age <= 10: return 100
    elif age <= 15: return 200
    elif age <= 20: return 300
    elif age <= 30: return 400
    elif age <= 40: return 350
    elif age <= 50: return 300
    elif age <= 65: return 250
    else: return 200

def get_age_prompt(age, topics):
    if age <= 10:
        return f"""You are Sparky, a friendly teacher for kids. 
        Use emojis (🌟🐘🎈) and short sentences. Suggested topics: {", ".join(topics)}. 
        If the child asks something else, still answer but keep it simple."""
    elif age <= 15:
        return f"""You are a cool, friendly older sibling. Keep it fun and safe. 
        Suggested topics: {", ".join(topics)}. Still answer other questions respectfully."""
    elif age <= 20:
        return f"""Be a supportive mentor. Provide clear explanations. 
        Suggested topics: {", ".join(topics)}. Allow curiosity beyond these topics."""
    elif age <= 30:
        return f"""Professional yet empathetic assistant. 
        Suggested topics: {", ".join(topics)}. Always answer even outside them."""
    elif age <= 40:
        return f"""Trustworthy and insightful guide. 
        Suggested topics: {", ".join(topics)}. Answer other queries with clarity."""
    elif age <= 50:
        return f"""Motivational coach with strategic advice. 
        Suggested topics: {", ".join(topics)}. Always stay supportive."""
    elif age <= 65:
        return f"""Respectful, wise, and practical advisor. 
        Suggested topics: {", ".join(topics)}. Other queries are welcome too."""
    else:
        return f"""Patient, polite, and gentle assistant. 
        Suggested topics: {", ".join(topics)}. Keep answers simple and respectful."""

def get_greeting(age):
    if age <= 10:
        return "Hello, friend! 😄 It's playtime! I'm Sparky. What fun thing should we do first?"
    elif age <= 15:
        return "Hey, what's up? 👋 I'm here for homework help, fun facts, or just a chat."
    elif age <= 20:
        return "Welcome! I can help with studies, career, or motivation. What's on your mind?"
    elif age <= 30:
        return "Hi there 👋 Life is busy, but I'm here to help with studies, jobs, or balance."
    elif age <= 40:
        return "Good to see you! Need practical advice, or just exploring ideas today?"
    elif age <= 50:
        return "Welcome! Let's plan your future, work goals, or maybe explore a new passion."
    elif age <= 65:
        return "Hello, it's a pleasure. I can help with wellness, finance, or leisure. What interests you?"
    else:
        return "Good day and welcome. Would you like a story, some information, or just a gentle chat?"

# -------------------------------
# Predefined Topics by Age
# -------------------------------
age_topics = {
    (0, 10): ["Alphabets", "Counting", "Stories", "Basic Shapes"],
    (11, 15): ["Fractions", "Geometry Basics", "Science Experiments", "History"],
    (16, 20): ["Integration", "Differentiation", "Physics", "Programming Basics"],
    (21, 25): ["Advanced Math", "Machine Learning", "Career Skills", "Philosophy"],
    (26, 35): ["Workplace Productivity", "Finance", "Parenting", "Technology"],
    (36, 50): ["Health", "Investments", "Leadership", "History"],
    (51, 65): ["Wellness", "Retirement Planning", "Travel", "Spirituality"],
    (66, 100): ["Memory Exercises", "Light Reading", "Health Care", "Gardening"]
}

def get_topics_for_age(age: int):
    for (low, high), topics in age_topics.items():
        if low <= age <= high:
            return topics
    return ["General Knowledge", "Stories", "Music"]

# -------------------------------
# Chatbot Class
# -------------------------------
class AgeBasedChatbot:
    def __init__(self, age, api_key):
        self.api_key = api_key
        self.set_age(age)

    def set_age(self, age):
        """Reconfigure chatbot when a new age is detected"""
        self.age = age
        topics = get_topics_for_age(age)
        system_prompt = get_age_prompt(age, topics)
        greeting = get_greeting(age)
        temperature = get_temperature(age)
        max_tokens = get_max_tokens(age)

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=temperature,
            max_output_tokens=max_tokens,
            google_api_key=self.api_key
        )

        # Reset conversation for new user
        self.messages = [
            SystemMessage(content=system_prompt),
            AIMessage(content=greeting)
        ]
        self.greeting = greeting
        self.topics = topics

    def chat(self, user_input):
        self.messages.append(HumanMessage(content=user_input))
        response = self.llm.invoke(self.messages)
        self.messages.append(response)
        print("resposne content:",response.content)  # save bot reply
        return {
            "reply": response.content, 
            "age": self.age,
            "suggested_topics": self.topics
        }