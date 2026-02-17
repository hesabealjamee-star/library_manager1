# services/book_service.py
from repositories.book_repo import BookRepo

class BookService:
    def __init__(self):
        self.repo = BookRepo()

    def list_all(self):
        return self.repo.list_all()

    def search(self, text):
        return self.repo.search(text)

    def add(self, title, author, category, isbn, total_copies):
        title = title.strip()
        author = author.strip()
        if not title or not author:
            raise ValueError("Title and Author are required.")
        if total_copies < 1:
            raise ValueError("Total copies must be >= 1.")
        self.repo.add(title, author, category.strip(), isbn.strip(), total_copies)

    def delete(self, book_id):
        self.repo.delete(book_id)
