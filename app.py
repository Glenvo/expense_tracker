
from app.gui_qt import ExpenseApp
from PyQt6.QtWidgets import QApplication
import sys
from app.db import init_db, drop_expenses_table
def main():
    init_db()     
    app = QApplication(sys.argv)
    window = ExpenseApp()
    window.show()
    sys.exit(app.exec())    
    
if __name__ == "__main__":
    main()
