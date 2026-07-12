from flask import Blueprint, request, jsonify
from models import Conversation, Message

conversation_bp = Blueprint('conversation', __name__)

@conversation_bp.route('/api/conversations', methods=['GET'])
def get_conversations():
    try:
        conversations = Conversation.get_all()
        return jsonify(conversations)
    except Exception:
        return jsonify({"error": "Failed to load conversations"}), 500

@conversation_bp.route('/api/conversations/<int:conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    try:
        conversation = Conversation.get_by_id(conversation_id)
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404

        messages = Message.get_by_conversation(conversation_id)
        conversation['messages'] = messages
        return jsonify(conversation)
    except Exception:
        return jsonify({"error": "Failed to load conversation"}), 500

@conversation_bp.route('/api/conversations', methods=['POST'])
def create_conversation():
    try:
        conversation_id = Conversation.create()
        conversation = Conversation.get_by_id(conversation_id)
        return jsonify(conversation), 201
    except Exception:
        return jsonify({"error": "Failed to create conversation"}), 500

@conversation_bp.route('/api/conversations/<int:conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    try:
        conversation = Conversation.get_by_id(conversation_id)
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404

        Conversation.delete(conversation_id)
        return jsonify({"message": "Conversation deleted"})
    except Exception:
        return jsonify({"error": "Failed to delete conversation"}), 500
