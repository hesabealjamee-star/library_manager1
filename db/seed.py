# db/seed.py
from db.connection import get_connection

def seed_data():
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM books;")
        if cur.fetchone()[0] == 0:
            cur.executemany("""
                INSERT INTO books(title, author, category, isbn, total_copies, available_copies)
                VALUES(?,?,?,?,?,?)
            """, [
                ("Clean Code", "Robert C. Martin", "Software", "9780132350884", 3, 3),
                ("Introduction to Algorithms", "Cormen", "Algorithms", "9780262033848", 2, 2),
                ("Database System Concepts", "Silberschatz", "Database", "9780073523323", 1, 1),
            ])

        cur.execute("SELECT COUNT(*) FROM members;")
        if cur.fetchone()[0] == 0:
            cur.executemany("""
                INSERT INTO members(full_name, phone, email)
                VALUES(?,?,?)
            """, [
                ("Aya Ahmad", "099999999", "aya@example.com"),
                ("Sara Ali", "088888888", "sara@example.com"),
            ])

        conn.commit()
