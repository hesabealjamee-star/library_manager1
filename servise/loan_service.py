# services/loan_service.py
from datetime import date, timedelta
from repositories.loan_repo import LoanRepo
from db.connection import get_connection

class LoanService:
    def __init__(self):
        self.repo = LoanRepo()

    def list_all(self):
        return self.repo.list_all()

    def borrow(self, book_id, member_id, days=7):
        # تحقق توفر الكتاب
        with get_connection() as conn:
            book = conn.execute("SELECT available_copies FROM books WHERE id=?;", (book_id,)).fetchone()
            if not book:
                raise ValueError("Book not found.")
            if book["available_copies"] <= 0:
                raise ValueError("This book is not available now.")

        loan_date = date.today().isoformat()
        due_date = (date.today() + timedelta(days=days)).isoformat()
        self.repo.create_loan(book_id, member_id, loan_date, due_date)

    def return_book(self, loan_id):
        self.repo.return_loan(loan_id, date.today().isoformat())
