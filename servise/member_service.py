# services/member_service.py
from repositories.member_repo import MemberRepo

class MemberService:
    def __init__(self):
        self.repo = MemberRepo()

    def list_all(self):
        return self.repo.list_all()

    def search(self, text):
        return self.repo.search(text)

    def add(self, full_name, phone, email):
        full_name = full_name.strip()
        if not full_name:
            raise ValueError("Full name is required.")
        self.repo.add(full_name, phone.strip(), email.strip())

    def delete(self, member_id):
        self.repo.delete(member_id)
