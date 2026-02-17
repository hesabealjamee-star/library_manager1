# repositories/member_repo.py
from db.connection import get_connection

class MemberRepo:
    def list_all(self):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM members ORDER BY id DESC;").fetchall()

    def search(self, text: str):
        q = f"%{text.strip()}%"
        with get_connection() as conn:
            return conn.execute("""
                SELECT * FROM members
                WHERE full_name LIKE ? OR phone LIKE ? OR email LIKE ?
                ORDER BY id DESC;
            """, (q, q, q)).fetchall()

    def add(self, full_name, phone, email):
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO members(full_name, phone, email)
                VALUES(?,?,?)
            """, (full_name, phone, email))
            conn.commit()

    def delete(self, member_id: int):
        with get_connection() as conn:
            conn.execute("DELETE FROM members WHERE id=?;", (member_id,))
            conn.commit()
