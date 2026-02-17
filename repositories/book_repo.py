# repositories/book_repo.py
from db.connection import get_connection

class BookRepo:
    def list_all(self):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM books ORDER BY id DESC;").fetchall()

    def search(self, text: str):
        q = f"%{text.strip()}%"
        with get_connection() as conn:
            return conn.execute("""
                SELECT * FROM books
                WHERE title LIKE ? OR author LIKE ? OR category LIKE ? OR isbn LIKE ?
                ORDER BY id DESC;
            """, (q, q, q, q)).fetchall()

    def add(self, title, author, category, isbn, total_copies):
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO books(title, author, category, isbn, total_copies, available_copies)
                VALUES(?,?,?,?,?,?)
            """, (title, author, category, isbn, total_copies, total_copies))
            conn.commit()

    def delete(self, book_id: int):
        with get_connection() as conn:
            conn.execute("DELETE FROM books WHERE id=?;", (book_id,))
            conn.commit()
