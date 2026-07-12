import groq
from config import Config

client = None

def initialize_client():
    global client
    api_key = Config.GROQ_API_KEY
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set. Add it to backend/.env")
    client = groq.Groq(api_key=api_key, timeout=30.0)

def _get_client():
    global client
    if not client:
        initialize_client()
    return client

SYSTEM_PROMPT = (
    "You are Veda, a helpful and intelligent AI assistant. "
    "Be concise, clear, and friendly. Format responses using markdown when appropriate."
)

def generate_response(conversation_history):
    c = _get_client()
    formatted_messages = []
    for msg in conversation_history:
        role = "user" if msg["role"] == "user" else "assistant"
        formatted_messages.append({"role": role, "content": msg["content"]})

    response = c.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, *formatted_messages],
        temperature=0.7,
        max_tokens=2048,
    )

    if not response.choices:
        raise ValueError("AI returned an empty response")
    content = response.choices[0].message.content
    if not content or not content.strip():
        raise ValueError("AI returned an empty response")
    return content.strip()

def generate_title(first_message):
    c = _get_client()
    response = c.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Generate a short, concise title (max 50 characters) for a conversation. Return ONLY the title, no quotes or extra text."},
            {"role": "user", "content": first_message[:500]}
        ],
        temperature=0.3,
        max_tokens=60,
    )
    if response.choices and response.choices[0].message.content:
        title = response.choices[0].message.content.strip().strip('"').strip("'")
        return title[:50] if title else first_message[:50].strip()
    return first_message[:50].strip()

def generate_response_stream(conversation_history):
    c = _get_client()
    formatted_messages = []
    for msg in conversation_history:
        role = "user" if msg["role"] == "user" else "assistant"
        formatted_messages.append({"role": role, "content": msg["content"]})

    return c.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, *formatted_messages],
        temperature=0.7,
        max_tokens=2048,
        stream=True,
    )
