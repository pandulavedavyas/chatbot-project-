from database import get_db_connection

class Conversation:
    @staticmethod
    def create(title="New Chat"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO conversations (title) VALUES (?)', (title,))
        conn.commit()
        conversation_id = cursor.lastrowid
        conn.close()
        return conversation_id
    
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM conversations ORDER BY updated_at DESC')
        conversations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return conversations
    
    @staticmethod
    def get_by_id(conversation_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM conversations WHERE id = ?', (conversation_id,))
        conversation = cursor.fetchone()
        conn.close()
        return dict(conversation) if conversation else None
    
    @staticmethod
    def update_title(conversation_id, title):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE conversations SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', 
                      (title, conversation_id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def update_timestamp(conversation_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?', 
                      (conversation_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete(conversation_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM messages WHERE conversation_id = ?', (conversation_id,))
        cursor.execute('DELETE FROM conversations WHERE id = ?', (conversation_id,))
        conn.commit()
        conn.close()

class Message:
    @staticmethod
    def create(conversation_id, role, content):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)',
                      (conversation_id, role, content))
        conn.commit()
        message_id = cursor.lastrowid
        Conversation.update_timestamp(conversation_id)
        conn.close()
        return message_id
    
    @staticmethod
    def get_by_conversation(conversation_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp', 
                      (conversation_id,))
        messages = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return messages
    
    @staticmethod
    def get_context(conversation_id):
        messages = Message.get_by_conversation(conversation_id)
        return [{"role": msg["role"], "content": msg["content"]} for msg in messages]
