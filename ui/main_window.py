# ui/main_window.py
from PySide6.QtWidgets import QMainWindow, QTabWidget
from ui.books_view import BooksView
from ui.members_view import MembersView
from ui.loans_view import LoansView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Manager")
        self.resize(1000, 650)

        tabs = QTabWidget()
        tabs.addTab(BooksView(), "Books")
        tabs.addTab(MembersView(), "Members")
        tabs.addTab(LoansView(), "Loans")

        self.setCentralWidget(tabs)
