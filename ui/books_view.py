# ui/books_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QSpinBox, QLabel
)
from services.book_service import BookService

class BooksView(QWidget):
    def __init__(self):
        super().__init__()
        self.service = BookService()

        layout = QVBoxLayout(self)

        # Top: Search
        top = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by title / author / category / isbn...")
        btn_search = QPushButton("Search")
        btn_refresh = QPushButton("Refresh")
        top.addWidget(self.search_input)
        top.addWidget(btn_search)
        top.addWidget(btn_refresh)
        layout.addLayout(top)

        # Form: Add Book
        form = QHBoxLayout()
        self.title_in = QLineEdit(); self.title_in.setPlaceholderText("Title*")
        self.author_in = QLineEdit(); self.author_in.setPlaceholderText("Author*")
        self.category_in = QLineEdit(); self.category_in.setPlaceholderText("Category")
        self.isbn_in = QLineEdit(); self.isbn_in.setPlaceholderText("ISBN")
        self.copies_in = QSpinBox(); self.copies_in.setMinimum(1); self.copies_in.setMaximum(999); self.copies_in.setValue(1)
        btn_add = QPushButton("Add")

        form.addWidget(QLabel("Add:"))
        form.addWidget(self.title_in)
        form.addWidget(self.author_in)
        form.addWidget(self.category_in)
        form.addWidget(self.isbn_in)
        form.addWidget(QLabel("Copies"))
        form.addWidget(self.copies_in)
        form.addWidget(btn_add)
        layout.addLayout(form)

        # Table
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "Category", "ISBN", "Total", "Available"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        # Bottom actions
        bottom = QHBoxLayout()
        btn_delete = QPushButton("Delete Selected")
        bottom.addWidget(btn_delete)
        bottom.addStretch()
        layout.addLayout(bottom)

        # Events
        btn_refresh.clicked.connect(self.load_data)
        btn_search.clicked.connect(self.search)
        btn_add.clicked.connect(self.add_book)
        btn_delete.clicked.connect(self.delete_selected)

        self.load_data()

    def load_data(self):
        rows = self.service.list_all()
        self.render(rows)

    def search(self):
        text = self.search_input.text().strip()
        rows = self.service.search(text) if text else self.service.list_all()
        self.render(rows)

    def render(self, rows):
        self.table.setRowCount(0)
        for r in rows:
            row_index = self.table.rowCount()
            self.table.insertRow(row_index)
            self.table.setItem(row_index, 0, QTableWidgetItem(str(r["id"])))
            self.table.setItem(row_index, 1, QTableWidgetItem(r["title"]))
            self.table.setItem(row_index, 2, QTableWidgetItem(r["author"]))
            self.table.setItem(row_index, 3, QTableWidgetItem(r["category"] or ""))
            self.table.setItem(row_index, 4, QTableWidgetItem(r["isbn"] or ""))
            self.table.setItem(row_index, 5, QTableWidgetItem(str(r["total_copies"])))
            self.table.setItem(row_index, 6, QTableWidgetItem(str(r["available_copies"])))

        self.table.resizeColumnsToContents()

    def add_book(self):
        try:
            self.service.add(
                self.title_in.text(),
                self.author_in.text(),
                self.category_in.text(),
                self.isbn_in.text(),
                int(self.copies_in.value())
            )
            self.title_in.clear()
            self.author_in.clear()
            self.category_in.clear()
            self.isbn_in.clear()
            self.copies_in.setValue(1)
            self.load_data()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def delete_selected(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Info", "Select a row first.")
            return
        book_id = int(self.table.item(row, 0).text())
        self.service.delete(book_id)
        self.load_data()
