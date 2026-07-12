from database import get_db_connection

class Conversation:
    @staticmethod
    def create(title="New Chat"):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO conversations (title) VALUES (?)', (title,))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM conversations ORDER BY updated_at DESC')
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def get_by_id(conversation_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM conversations WHERE id = ?', (conversation_id,))
            conversation = cursor.fetchone()
            return dict(conversation) if conversation else None
        finally:
            conn.close()

    @staticmethod
    def update_title(conversation_id, title):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('UPDATE conversations SET title = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                          (title, conversation_id))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def update_timestamp(conversation_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                          (conversation_id,))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete(conversation_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM conversations WHERE id = ?', (conversation_id,))
            conn.commit()
        finally:
            conn.close()

class Message:
    @staticmethod
    def create(conversation_id, role, content):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)',
                          (conversation_id, role, content))
            conn.commit()
            cursor.execute('UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = ?', (conversation_id,))
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_by_conversation(conversation_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp',
                          (conversation_id,))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def get_context(conversation_id):
        messages = Message.get_by_conversation(conversation_id)
        return [{"role": msg["role"], "content": msg["content"]} for msg in messages]

    @staticmethod
    def delete_last_user_message(conversation_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM messages WHERE id = (SELECT id FROM messages WHERE conversation_id = ? AND role = ? ORDER BY id DESC LIMIT 1)',
                (conversation_id, 'user')
            )
            conn.commit()
        finally:
            conn.close()
