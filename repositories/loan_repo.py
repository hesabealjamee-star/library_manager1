# repositories/loan_repo.py
from db.connection import get_connection

class LoanRepo:
    def list_all(self):
        with get_connection() as conn:
            return conn.execute("""
                SELECT l.*, b.title AS book_title, m.full_name AS member_name
                FROM loans l
                JOIN books b ON b.id = l.book_id
                JOIN members m ON m.id = l.member_id
                ORDER BY l.id DESC;
            """).fetchall()

    def create_loan(self, book_id, member_id, loan_date, due_date):
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO loans(book_id, member_id, loan_date, due_date, status)
                VALUES(?,?,?,?, 'BORROWED');
            """, (book_id, member_id, loan_date, due_date))

            conn.execute("""
                UPDATE books
                SET available_copies = available_copies - 1
                WHERE id=? AND available_copies > 0;
            """, (book_id,))
            conn.commit()

    def return_loan(self, loan_id, return_date):
        with get_connection() as conn:
            # احضار book_id
            row = conn.execute("SELECT book_id FROM loans WHERE id=?;", (loan_id,)).fetchone()
            if not row:
                return
            book_id = row["book_id"]

            conn.execute("""
                UPDATE loans
                SET return_date=?, status='RETURNED'
                WHERE id=?;
            """, (return_date, loan_id))

            conn.execute("""
                UPDATE books
                SET available_copies = available_copies + 1
                WHERE id=?;
            """, (book_id,))
            conn.commit()
