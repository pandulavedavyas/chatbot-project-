from database import get_db_connection, release_conn, _q, _dict_row, _dict_all, USE_POSTGRES

class Conversation:
    @staticmethod
    def create(title="New Chat"):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute(f'INSERT INTO conversations (title) VALUES ({_q(1)}) RETURNING id', (title,))
                conn.commit()
                return cursor.fetchone()[0]
            else:
                cursor.execute(f'INSERT INTO conversations (title) VALUES ({_q(1)})', (title,))
                conn.commit()
                return cursor.lastrowid
        finally:
            release_conn(conn)

    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM conversations ORDER BY updated_at DESC')
            return _dict_all(cursor)
        finally:
            release_conn(conn)

    @staticmethod
    def get_by_id(conversation_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM conversations WHERE id = {_q(1)}', (conversation_id,))
            return _dict_row(cursor)
        finally:
            release_conn(conn)

    @staticmethod
    def update_title(conversation_id, title):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(f'UPDATE conversations SET title = {_q(1)}, updated_at = CURRENT_TIMESTAMP WHERE id = {_q(1)}',
                          (title, conversation_id))
            conn.commit()
        finally:
            release_conn(conn)

    @staticmethod
    def update_timestamp(conversation_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(f'UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = {_q(1)}',
                          (conversation_id,))
            conn.commit()
        finally:
            release_conn(conn)

    @staticmethod
    def delete(conversation_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(f'DELETE FROM conversations WHERE id = {_q(1)}', (conversation_id,))
            conn.commit()
        finally:
            release_conn(conn)

class Message:
    @staticmethod
    def create(conversation_id, role, content):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute(f'INSERT INTO messages (conversation_id, role, content) VALUES ({_q(3)}) RETURNING id',
                              (conversation_id, role, content))
                conn.commit()
                msg_id = cursor.fetchone()[0]
            else:
                cursor.execute(f'INSERT INTO messages (conversation_id, role, content) VALUES ({_q(3)})',
                              (conversation_id, role, content))
                conn.commit()
                msg_id = cursor.lastrowid
            cursor.execute(f'UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = {_q(1)}', (conversation_id,))
            conn.commit()
            return msg_id
        finally:
            release_conn(conn)

    @staticmethod
    def get_by_conversation(conversation_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(f'SELECT * FROM messages WHERE conversation_id = {_q(1)} ORDER BY timestamp',
                          (conversation_id,))
            return _dict_all(cursor)
        finally:
            release_conn(conn)

    @staticmethod
    def get_context(conversation_id):
        messages = Message.get_by_conversation(conversation_id)
        return [{"role": msg["role"], "content": msg["content"]} for msg in messages]

    @staticmethod
    def delete_last_user_message(conversation_id):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            if USE_POSTGRES:
                cursor.execute(
                    'DELETE FROM messages WHERE id = (SELECT id FROM messages WHERE conversation_id = %s AND role = %s ORDER BY id DESC LIMIT 1)',
                    (conversation_id, 'user')
                )
            else:
                cursor.execute(
                    'DELETE FROM messages WHERE id = (SELECT id FROM messages WHERE conversation_id = ? AND role = ? ORDER BY id DESC LIMIT 1)',
                    (conversation_id, 'user')
                )
            conn.commit()
        finally:
            release_conn(conn)
