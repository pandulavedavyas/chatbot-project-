from flask import Blueprint, request, jsonify
from models import Conversation, Message
from services.gemini_service import generate_response, generate_title
from utils.helpers import validate_message, validate_conversation_id, format_conversation_title

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({"error": "Message is required"}), 400
    
    message = data['message']
    conversation_id = data.get('conversation_id')
    
    if not validate_message(message):
        return jsonify({"error": "Invalid message"}), 400
    
    try:
        if not conversation_id:
            conversation_id = Conversation.create()
            try:
                title = generate_title(message)
                Conversation.update_title(conversation_id, format_conversation_title(title))
            except Exception as e:
                print(f"Title generation failed: {e}")
                Conversation.update_title(conversation_id, format_conversation_title(message))
        
        if not validate_conversation_id(conversation_id):
            return jsonify({"error": "Invalid conversation_id"}), 400
        
        conversation = Conversation.get_by_id(conversation_id)
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404
        
        Message.create(conversation_id, 'user', message)
        
        conversation_history = Message.get_context(conversation_id)
        
        ai_response = generate_response(conversation_history)
        
        Message.create(conversation_id, 'assistant', ai_response)
        
        return jsonify({
            "reply": ai_response,
            "conversation_id": conversation_id
        })
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({"error": f"Failed to generate response: {str(e)}"}), 500
