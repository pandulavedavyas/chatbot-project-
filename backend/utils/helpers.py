def format_conversation_title(message, max_length=50):
    if not message or not message.strip():
        return "New Chat"
    message = message.strip()
    if len(message) <= max_length:
        return message
    truncated = message[:max_length]
    last_space = truncated.rfind(' ')
    if last_space > 0:
        return truncated[:last_space] + '...'
    return truncated + '...'

def validate_message(message):
    if not message or not isinstance(message, str):
        return False
    if len(message.strip()) == 0:
        return False
    return True

def validate_conversation_id(conversation_id):
    if conversation_id is None:
        return False
    if isinstance(conversation_id, float):
        conversation_id = int(conversation_id)
    if not isinstance(conversation_id, int) or conversation_id <= 0:
        return False
    return True
