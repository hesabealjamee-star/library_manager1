# main.py
import sys
from PySide6.QtWidgets import QApplication

from db.schema import create_tables
from db.seed import seed_data
from ui.main_window import MainWindow

def main():
    create_tables()
    seed_data()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
