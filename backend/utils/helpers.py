def format_conversation_title(message, max_length=50):
    if len(message) <= max_length:
        return message
    return message[:max_length].rsplit(' ', 1)[0] + '...'

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
