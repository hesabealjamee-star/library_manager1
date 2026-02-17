# ui/members_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QLabel
)
from services.member_service import MemberService

class MembersView(QWidget):
    def __init__(self):
        super().__init__()
        self.service = MemberService()

        layout = QVBoxLayout(self)

        top = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name / phone / email...")
        btn_search = QPushButton("Search")
        btn_refresh = QPushButton("Refresh")
        top.addWidget(self.search_input)
        top.addWidget(btn_search)
        top.addWidget(btn_refresh)
        layout.addLayout(top)

        form = QHBoxLayout()
        self.name_in = QLineEdit(); self.name_in.setPlaceholderText("Full name*")
        self.phone_in = QLineEdit(); self.phone_in.setPlaceholderText("Phone")
        self.email_in = QLineEdit(); self.email_in.setPlaceholderText("Email")
        btn_add = QPushButton("Add")

        form.addWidget(QLabel("Add:"))
        form.addWidget(self.name_in)
        form.addWidget(self.phone_in)
        form.addWidget(self.email_in)
        form.addWidget(btn_add)
        layout.addLayout(form)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Full Name", "Phone", "Email"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        bottom = QHBoxLayout()
        btn_delete = QPushButton("Delete Selected")
        bottom.addWidget(btn_delete)
        bottom.addStretch()
        layout.addLayout(bottom)

        btn_refresh.clicked.connect(self.load_data)
        btn_search.clicked.connect(self.search)
        btn_add.clicked.connect(self.add_member)
        btn_delete.clicked.connect(self.delete_selected)

        self.load_data()

    def load_data(self):
        self.render(self.service.list_all())

    def search(self):
        text = self.search_input.text().strip()
        self.render(self.service.search(text) if text else self.service.list_all())

    def render(self, rows):
        self.table.setRowCount(0)
        for r in rows:
            i = self.table.rowCount()
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(r["id"])))
            self.table.setItem(i, 1, QTableWidgetItem(r["full_name"]))
            self.table.setItem(i, 2, QTableWidgetItem(r["phone"] or ""))
            self.table.setItem(i, 3, QTableWidgetItem(r["email"] or ""))
        self.table.resizeColumnsToContents()

    def add_member(self):
        try:
            self.service.add(self.name_in.text(), self.phone_in.text(), self.email_in.text())
            self.name_in.clear(); self.phone_in.clear(); self.email_in.clear()
            self.load_data()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def delete_selected(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Info", "Select a row first.")
            return
        member_id = int(self.table.item(row, 0).text())
        self.service.delete(member_id)
        self.load_data()
