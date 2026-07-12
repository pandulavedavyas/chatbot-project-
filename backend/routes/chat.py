from flask import Blueprint, request, jsonify, Response
from models import Conversation, Message
from services.ai_service import generate_response, generate_title, generate_response_stream
from utils.helpers import validate_message, validate_conversation_id, format_conversation_title
from config import Config
import json

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True)

    if not data or 'message' not in data:
        return jsonify({"error": "Message is required"}), 400

    message = data['message']
    conversation_id = data.get('conversation_id')
    stream = data.get('stream', False)

    if not validate_message(message):
        return jsonify({"error": "Invalid or empty message"}), 400

    if len(message) > Config.MAX_MESSAGE_LENGTH:
        return jsonify({"error": f"Message exceeds maximum length of {Config.MAX_MESSAGE_LENGTH} characters"}), 400

    try:
        if conversation_id is None:
            conversation_id = Conversation.create()
            try:
                title = generate_title(message)
                Conversation.update_title(conversation_id, format_conversation_title(title))
            except Exception:
                Conversation.update_title(conversation_id, format_conversation_title(message))

        if not validate_conversation_id(conversation_id):
            return jsonify({"error": "Invalid conversation_id"}), 400

        conversation = Conversation.get_by_id(conversation_id)
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404

        Message.create(conversation_id, 'user', message)
        conversation_history = Message.get_context(conversation_id)

        if stream:
            return _stream_response(conversation_id, conversation_history)

        try:
            ai_response = generate_response(conversation_history)
        except Exception:
            Message.delete_last_user_message(conversation_id)
            raise

        Message.create(conversation_id, 'assistant', ai_response)

        return jsonify({
            "reply": ai_response,
            "conversation_id": conversation_id
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Failed to generate response. Please try again."}), 500


def _stream_response(conversation_id, conversation_history):
    full_response = []

    def generate():
        try:
            stream = generate_response_stream(conversation_history)
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    token = chunk.choices[0].delta.content
                    full_response.append(token)
                    yield f"data: {json.dumps({'token': token, 'done': False})}\n\n"

            complete_response = ''.join(full_response).strip()
            if complete_response:
                Message.create(conversation_id, 'assistant', complete_response)

            yield f"data: {json.dumps({'token': '', 'done': True, 'conversation_id': conversation_id})}\n\n"
        except Exception:
            Message.delete_last_user_message(conversation_id)
            yield f"data: {json.dumps({'token': '', 'done': True, 'error': 'Failed to generate response'})}\n\n"

    return Response(generate(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})
