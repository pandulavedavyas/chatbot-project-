import groq
from config import Config

client = None

def initialize_client():
    global client
    api_key = Config.GROQ_API_KEY
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set. Add it to backend/.env")
    client = groq.Groq(api_key=api_key)

def generate_response(conversation_history):
    global client
    if not client:
        initialize_client()

    try:
        formatted_messages = []
        for msg in conversation_history:
            role = "user" if msg["role"] == "user" else "assistant"
            formatted_messages.append({
                "role": role,
                "content": msg["content"]
            })

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Veda, a helpful and intelligent AI assistant. Be concise, clear, and friendly. Format responses using markdown when appropriate."},
                *formatted_messages
            ],
            temperature=0.7,
            max_tokens=2048,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating response: {e}")
        raise e

def generate_title(first_message):
    global client
    if not client:
        initialize_client()

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Generate a short, concise title (max 50 characters) for a conversation. Return ONLY the title, no quotes or extra text."},
                {"role": "user", "content": first_message}
            ],
            temperature=0.3,
            max_tokens=60,
        )
        return response.choices[0].message.content.strip().strip('"').strip("'")
    except Exception as e:
        print(f"Error generating title: {e}")
        return first_message[:50]
